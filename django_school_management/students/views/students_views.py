from datetime import date, timedelta, datetime
from collections import OrderedDict

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from django_school_management.academics.models import (
    Department,
    Semester,
    Batch,
    AcademicSession,
)
from django_school_management.mixins.no_permission import (
    LoginRequiredNoPermissionMixin,
)
from django_school_management.result.models import SubjectGroup
from django_school_management.students.models import (
    Student,
    AdmissionStudent,
    CounselingComment,
)
from django_school_management.students.forms import (
    StudentForm,
    AdmissionForm,
    StudentRegistrantUpdateForm,
    CounselingDataForm,
    StudentUpdateForm,
)
from django_school_management.students.filters import AlumniFilter
from django_school_management.students.tasks import (
    send_admission_confirmation_email,
)
from permission_handlers.administrative import (
    user_is_admin_su_or_ac_officer,
)
from permission_handlers.basic import user_is_student, user_is_verified
from django_school_management.mixins.institute import get_user_institute


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_dashboard_index(request):
    """
    Dashboard for online admission system.
    """
    institute = get_user_institute(request.user)

    # List of months since first application registration date
    try:
        first_application_date = datetime.strftime(
            datetime.now() - timedelta(days=365), "%Y-%m-%d"
        )
        last_application_date = date.today()
        dates = [str(first_application_date), str(last_application_date)]
        months_start, months_end = [
            datetime.strptime(_, "%Y-%m-%d") for _ in dates
        ]
        month_list = OrderedDict(
            ((months_start + timedelta(_)).strftime(r"%B-%Y"), None)
            for _ in range((months_end - months_start).days)
        ).keys()
    except IndexError:
        month_list = []

    base_qs = AdmissionStudent.objects.filter(assigned_as_student=False)
    if institute:
        base_qs = base_qs.filter(department_choice__institute=institute)

    unpaid_registrants = base_qs.filter(paid=False)
    all_applicants = base_qs.order_by("-created")
    admitted_students = base_qs.filter(admitted=True, paid=True)
    paid_registrants = base_qs.filter(paid=True, admitted=False)
    rejected_applicants = base_qs.filter(rejected=True)
    offline_applicants = base_qs.filter(application_type="2")

    context = {
        "all_applicants": all_applicants,
        "unpaid_registrants": unpaid_registrants,
        "admitted_students": admitted_students,
        "paid_registrants": paid_registrants,
        "rejected_applicants": rejected_applicants,
        "offline_applicants": offline_applicants,
        "month_list": month_list,
    }
    return render(request, "students/dashboard_index.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def all_applicants(request):
    """Display all registered students list"""
    institute = get_user_institute(request.user)
    registrants = AdmissionStudent.objects.all().order_by("-created")
    if institute:
        registrants = registrants.filter(department_choice__institute=institute)
    ctx = {
        "registrants": registrants,
    }
    return render(request, "students/all_applicants.html", ctx)


@user_passes_test(user_is_admin_su_or_ac_officer)
def admitted_students_list(request):
    """
    Returns list of students admitted from online registration.
    """
    admitted_students = AdmissionStudent.objects.filter(
        admitted=True, paid=True, assigned_as_student=False
    )
    context = {
        "admitted_students": admitted_students,
    }
    return render(
        request, "students/dashboard_all_cleared_students.html", context
    )


@user_passes_test(user_is_admin_su_or_ac_officer)
def paid_registrants(request):
    """
    Returns list of students already paid from online registration.
    """
    paid_students = AdmissionStudent.objects.filter(paid=True, admitted=False)
    context = {
        "paid_students": paid_students,
    }
    return render(request, "students/dashboard_paid_students.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def unpaid_registrants(request):
    """
    Returns list of students haven't paid admission fee yet.
    """
    unpaid_registrants_list = AdmissionStudent.objects.filter(paid=False)
    context = {
        "unpaid_applicants": unpaid_registrants_list,
    }
    return render(request, "students/unpaid_applicants.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def rejected_registrants(request):
    ctx = {
        "rejected_registrants": AdmissionStudent.objects.filter(rejected=True),
    }
    return render(request, "students/list/rejected_registrants.html", ctx)


def get_json_batch_data(request, *args, **kwargs):
    """Return batches for the given department, restricted to the active academic session."""
    selected_department_code = kwargs.get("department_code")
    active_session = AcademicSession.objects.order_by("-year").first()
    qs = Batch.objects.filter(department__code=selected_department_code)
    if active_session:
        qs = qs.filter(year=active_session)
    department_batches = list(qs.values())
    return JsonResponse({"data": department_batches})


@user_passes_test(user_is_admin_su_or_ac_officer)
def admission_confirmation(request):
    """
    Create student profiles from admitted applicants. Applicants are already
    assigned to a department; filter by department (and batch for active session).
    Session is derived from the chosen batch; no session dropdown.
    """
    active_session = AcademicSession.objects.order_by("-year").first()
    base_registrants = AdmissionStudent.objects.filter(
        admitted=True, paid=True, rejected=False, assigned_as_student=False
    )
    departments = Department.objects.order_by("name")

    department_id = request.GET.get("department_id")
    batch_id_param = request.GET.get("batch_id")

    if department_id:
        try:
            selected_department_id = int(department_id)
            selected_registrants = base_registrants.filter(
                choosen_department_id=selected_department_id
            )
            batches = (
                Batch.objects.filter(
                    department_id=selected_department_id,
                    year=active_session,
                )
                .order_by("number")
                if active_session
                else Batch.objects.none()
            )
        except (ValueError, TypeError):
            selected_department_id = None
            selected_registrants = base_registrants.none()
            batches = Batch.objects.none()
    else:
        selected_department_id = None
        selected_registrants = base_registrants.none()
        batches = Batch.objects.none()

    try:
        selected_batch_id_val = int(batch_id_param) if batch_id_param else None
    except (ValueError, TypeError):
        selected_batch_id_val = None

    ctx = {
        "departments": departments,
        "active_session": active_session,
        "no_active_session": active_session is None,
        "selected_registrants": selected_registrants,
        "selected_department_id": selected_department_id,
        "selected_batch_id": selected_batch_id_val,
        "batches": batches,
    }

    if request.method == "POST":
        batch_id = request.POST.get("batch_id")
        checked_registrant_ids = [x.strip() for x in request.POST.getlist("registrant_choice") if x.strip()]

        if not batch_id:
            messages.error(request, "Please select a batch.")
            return render(request, "students/list/confirm_admission.html", ctx)

        if not checked_registrant_ids:
            messages.error(request, "Please select at least one applicant.")
            return render(request, "students/list/confirm_admission.html", ctx)

        try:
            batch = Batch.objects.get(id=batch_id)
        except (Batch.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select or create a batch first.")
            return render(request, "students/list/confirm_admission.html", ctx)

        session = batch.year
        if active_session and session != active_session:
            messages.error(
                request,
                "Selected batch is not in the current academic session.",
            )
            return render(request, "students/list/confirm_admission.html", ctx)

        try:
            ids = [int(x) for x in checked_registrant_ids]
        except (ValueError, TypeError):
            messages.error(request, "Invalid applicant selection.")
            return render(request, "students/list/confirm_admission.html", ctx)

        to_be_admitted = base_registrants.filter(id__in=ids)
        invalid = to_be_admitted.exclude(choosen_department_id=batch.department_id)
        if invalid.exists():
            messages.error(
                request,
                "All selected applicants must belong to the chosen batch's department.",
            )
            return render(request, "students/list/confirm_admission.html", ctx)

        semester_number = 1
        try:
            semester = Semester.objects.get(number=semester_number)
        except Semester.DoesNotExist:
            messages.error(
                request,
                f"Semester {semester_number} not found! Please create it first.",
            )
            return render(request, "students/list/confirm_admission.html", ctx)

        students = []
        errors = []
        with transaction.atomic():
            for candidate in to_be_admitted:
                try:
                    student = Student.objects.create(
                        admission_student=candidate,
                        semester=semester,
                        batch=batch,
                        ac_session=session,
                        admitted_by=request.user,
                    )
                    students.append(student)
                except Exception as e:
                    errors.append(f"{candidate.name}: {e}")

        if students:
            messages.success(
                request, f"{len(students)} student(s) created successfully."
            )
        if errors:
            for err in errors:
                messages.error(request, err)

        if students:
            return redirect("students:admission_confirmation")
        ctx["students"] = students
        return render(request, "students/list/confirm_admission.html", ctx)

    return render(request, "students/list/confirm_admission.html", ctx)


@user_passes_test(user_is_admin_su_or_ac_officer)
def admit_student(request, pk):
    """
    Admit applicant found by id/pk into chosen department.
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == "POST":
        form = AdmissionForm(request.POST, instance=applicant)
        if form.is_valid():
            student = form.save(commit=False)
            student.admitted = True
            student.admission_date = date.today()
            student.save()
            try:
                send_admission_confirmation_email.delay(student.id)
            except Exception:
                pass
            messages.success(request, f"{applicant.name} has been admitted.")
            return redirect("students:admitted_student_list")
    else:
        form = AdmissionForm(instance=applicant)
    context = {"form": form, "applicant": applicant}
    return render(request, "students/dashboard_admit_student.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def reject_applicant(request, pk):
    """Reject an applicant with an optional reason."""
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == "POST":
        applicant.rejected = True
        applicant.admitted = False
        applicant.save()
        messages.success(request, f"{applicant.name} has been rejected.")
    return redirect("students:all_applicants")


@user_passes_test(user_is_admin_su_or_ac_officer)
def mark_as_paid_or_unpaid(request):
    """Change student applicants payment status"""
    if request.method == "POST":
        registrant_pk = request.POST.get("registrant_id")
        applicant = get_object_or_404(AdmissionStudent, pk=registrant_pk)
        if not applicant.paid:
            # If applicant didn't pay fee already, change to paid
            applicant.paid = True
            applicant.save()
            return JsonResponse({"data": True})
        # If applicant already paid the amount, change to unpaid
        applicant.paid = False
        applicant.save()
        return JsonResponse({"data": False})


@user_passes_test(user_is_admin_su_or_ac_officer)
def update_online_registrant(request, pk):
    """Update applicant details and counseling information."""
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    counseling_records = CounselingComment.objects.filter(
        registrant_student=applicant
    )
    if request.method == "POST":
        form = StudentRegistrantUpdateForm(
            request.POST, request.FILES, instance=applicant
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"{applicant.name} updated.")
            return redirect("students:all_applicants")
    else:
        form = StudentRegistrantUpdateForm(instance=applicant)
    counseling_form = CounselingDataForm()
    context = {
        "form": form,
        "applicant": applicant,
        "counseling_records": counseling_records,
        "counseling_form": counseling_form,
    }
    return render(
        request, "students/dashboard_update_online_applicant.html", context
    )


@user_passes_test(user_is_admin_su_or_ac_officer)
def add_counseling_data(request, student_id):
    registrant = get_object_or_404(AdmissionStudent, id=student_id)
    if request.method == "POST":
        form = CounselingDataForm(request.POST)
        if form.is_valid():
            counseling_comment = form.save(commit=False)
            counseling_comment.counselor = request.user
            counseling_comment.registrant_student = registrant
            counseling_comment.save()
            return redirect("students:update_online_registrant", pk=student_id)


@user_passes_test(user_is_admin_su_or_ac_officer)
def add_student_view(request):
    """Offline admission form."""
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.application_type = "2"
            student.save()
            messages.success(request, f"{student.name} added as offline applicant.")
            return redirect("students:all_applicants")
    else:
        form = StudentForm()
    context = {"form": form}
    return render(request, "students/addstudent.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_view(request):
    """
    :param request:
    :return: renders student list with all department
    and semesters list.
    """
    institute = get_user_institute(request.user)
    all_students = Student.objects.select_related(
        "admission_student", "semester", "ac_session"
    ).all()
    if institute:
        all_students = all_students.filter(
            admission_student__choosen_department__institute=institute
        )
    context = {
        "students": all_students,
    }
    return render(request, "students/list/students_list.html", context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    students = Student.objects.select_related(
        "department", "semester", "ac_session"
    ).filter(department=dept_name)
    context = {
        "students": students,
    }
    return render(request, "students/students_by_department.html", context)


class StudentUpdateView(
    LoginRequiredNoPermissionMixin, UserPassesTestMixin, UpdateView
):
    """
    renders a student update form to update students details.
    """

    model = Student
    form_class = StudentUpdateForm
    template_name = "students/update_student.html"

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def post(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Student, pk=pk)
        form = StudentUpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("students:student_details", pk=obj.pk)

    def get_success_url(self):
        student_id = self.kwargs["pk"]
        return reverse_lazy(
            "students:student_details", kwargs={"pk": student_id}
        )


class StudentDetailsView(
    LoginRequiredNoPermissionMixin, UserPassesTestMixin, DetailView
):
    model = Student
    template_name = "students/student_details.html"

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = kwargs["object"]
        pk = obj.id
        student = Student.objects.get(pk=pk)
        # get student object
        # for showing subjects in option form
        student_subject_qs = SubjectGroup.objects.filter(
            department=student.admission_student.choosen_department,
            semester=student.semester,
        )
        context["subjects"] = student_subject_qs
        # getting result objects
        results = student.results.all()
        context["results"] = results
        return context


@user_passes_test(user_is_admin_su_or_ac_officer)
def student_delete_view(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect("students:all_student")


class AlumnusListView(
    LoginRequiredNoPermissionMixin, UserPassesTestMixin, ListView
):
    model = Student
    context_object_name = "alumnus"
    template_name = "students/list/alumnus.html"

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def get_queryset(self):
        queryset = Student.alumnus.all()
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        ctx = super().get_context_data(
            *args, object_list=object_list, **kwargs
        )
        alumnus = Student.alumnus.all()
        f = AlumniFilter(self.request.GET, queryset=alumnus)
        ctx["filter"] = f
        return ctx


@user_passes_test(user_is_student)
def student_my_portal(request, student_id: str):
    if request.user.employee_or_student_id != student_id:
        return HttpResponseNotFound("Page not found!")

    student = Student.objects.get(temporary_id=student_id)

    department = student.admission_student.choosen_department
    subject_group = SubjectGroup.objects.filter(
        department=department, semester=student.semester
    ).first()
    ctx = {"student": student, "subjects": subject_group.subjects.all()}
    return render(request, "students/my-portal.html", ctx)
