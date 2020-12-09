from datetime import date, timedelta, datetime
from collections import OrderedDict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from academics.views import user_is_staff
from academics.models import Department, Semester, Subject, Batch
from students.models import Student, AdmissionStudent, CounselingComment
from students.forms import (StudentForm, AdmissionForm,
                            StudentRegistrantUpdateForm,
                            CounselingDataForm)

from students.tasks import send_admission_confirmation_email


@user_passes_test(user_is_staff)
def students_dashboard_index(request):
    """
    Dashboard for online admission system. 
    """
    online_applicants = AdmissionStudent.objects.filter(paid=False)
    all_applicants = AdmissionStudent.objects.all().order_by('-created')
    admitted_students = AdmissionStudent.objects.filter(admitted=True, paid=True)
    paid_registrants = AdmissionStudent.objects.filter(paid=True, admitted=False)
    rejected_applicants = AdmissionStudent.objects.filter(rejected=True)

    # List of months since first application registration date
    first_application_date = AdmissionStudent.objects.order_by('created')[0].created.date()
    last_application_date = date.today()
    dates = [str(first_application_date), str(last_application_date)]
    print(dates)
    months_start, months_end = [datetime.strptime(_, '%Y-%m-%d') for _ in dates]
    # List of month to display options in student dashboard index
    month_list = OrderedDict(((months_start + timedelta(_)).strftime(r"%B-%Y"), None) for _ in
                            range((months_end - months_start).days)).keys()
    print(month_list)
    context = {
        'all_applicants': all_applicants,
        'online_applicants': online_applicants,
        'admitted_students': admitted_students,
        'paid_registrants': paid_registrants,
        'rejected_applicants': rejected_applicants,
        'month_list': month_list,
    }
    return render(request, 'students/dashboard_index.html', context)


@user_passes_test(user_is_staff)
def all_applicants(request):
    """Display all registered students list"""
    registrants = AdmissionStudent.objects.all().order_by('-created')
    ctx = {
        'registrants': registrants,
    }
    return render(request, 'students/all_applicants.html', ctx)


@user_passes_test(user_is_staff)
def admitted_students_list(request):
    """ 
    Returns list of students admitted from online registration.
    """
    admitted_students = AdmissionStudent.objects.filter(admitted=True, paid=True)
    context = {
        'admitted_students': admitted_students,
    }
    return render(request, 'students/dashboard_admitted_students.html', context)


@user_passes_test(user_is_staff)
def paid_registrants(request):
    """ 
    Returns list of students already paid from online registration.
    """
    paid_students = AdmissionStudent.objects.filter(paid=True, admitted=False)
    context = {
        'paid_students': paid_students,
    }
    return render(request, 'students/dashboard_paid_students.html', context)


@user_passes_test(user_is_staff)
def unpaid_registrants(request):
    """
    Returns list of students haven't paid admission fee yet.
    """
    unpaid_registrants_list = AdmissionStudent.objects.filter(paid=False)
    context = {
        'unpaid_applicants': unpaid_registrants_list,
    }
    return render(request, 'students/unpaid_applicants.html', context)


@user_passes_test(user_is_staff)
def rejected_registrants(request):
    ctx = {
        'rejected_registrants': AdmissionStudent.objects.filter(rejected=True),
    }
    return render(request, 'students/list/rejected_registrants.html', ctx)


@user_passes_test(user_is_staff)
def amission_confirmation(request):
    """
    If request is get, show list of applicants to be admitted finally as student,
    for POST request, it will create Student, RegularStudent.
    """
    selected_registrants = AdmissionStudent.objects.filter(
        admitted=True, 
        paid=True, 
        rejected=False
    )
    departments = Department.objects.order_by('name')
    batches = Batch.objects.all()
    # student_candidates = Student.objects
    ctx = {
        'selected_registrants': selected_registrants,
        'departments': departments,
        'batches': batches
    }
    
    if request.method == 'GET' and request.GET.get('dept') and request.GET.get('batch'):
        pass
        # Handle form submission

    if request.method == 'POST':
        return
    else:
        return render(request, 'students/list/confirm_admission.html', ctx)


@user_passes_test(user_is_staff)
def admit_student(request, pk):
    """ 
    Admit applicant found by id/pk into chosen department
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=applicant)
        if form.is_valid():
            student = form.save(commit=False)
            student.admitted = True
            student.paid = True
            student.admission_date = date.today()
            student.save()
            send_admission_confirmation_email.delay(student.id)
            return redirect('students:admitted_student_list')
    else:
        form = AdmissionForm()
        context = {'form': form, 'applicant': applicant}
    return render(request, 'students/dashboard_admit_student.html', context)


def mark_as_paid_or_unpaid(request):
    """ Change student applicants payment status """
    if request.method == 'POST':
        registrant_pk = request.POST.get('registrant_id')
        applicant = get_object_or_404(AdmissionStudent, pk=registrant_pk)
        if not applicant.paid:
            # If applicant didn't pay fee already, change to paid
            applicant.paid = True
            applicant.save()
            return JsonResponse({'data': True})
        # If applicant already paid the amount, change to unpaid
        applicant.paid = False
        applicant.save()
        return JsonResponse({'data': False})


@user_passes_test(user_is_staff)
def update_online_registrant(request, pk):
    """ 
    Update applicants details, counseling information
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    counseling_records = CounselingComment.objects.filter(registrant_student=applicant)
    if request.method == 'POST':
        form = StudentRegistrantUpdateForm(
            request.POST,
            request.FILES,
            instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('students:paid_registrants')
    else:
        form = StudentRegistrantUpdateForm(instance=applicant)
        counseling_form = CounselingDataForm()
        context = {
            'form': form,
            'applicant': applicant,
            'counseling_records': counseling_records,
            'counseling_form': counseling_form}
    return render(request, 'students/dashboard_update_online_applicant.html', context)


@user_passes_test(user_is_staff)
def add_counseling_data(request, student_id):
    registrant = get_object_or_404(AdmissionStudent, id=student_id)
    if request.method == 'POST':
        form = CounselingDataForm(request.POST)
        if form.is_valid():
            counseling_comment = form.save(commit=False)
            # TODO: NEEDS IMPROVEMENT
            # counseling_comment.counselor = "SHOULD BE A USER/COUNSELOR"
            counseling_comment.registrant_student = registrant
            counseling_comment.save()
            return redirect('students:update_online_registrant', pk=student_id)


@user_passes_test(user_is_staff)
def add_student_view(request):
    """
    :param request:
    :return: admission form to
    logged in user.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            # check student as offline registration
            student.application_type = '2'
            student.save()
            pk = form.instance.pk
            return redirect('students:student_details', pk=pk)
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'students/addstudent.html', context)


@user_passes_test(user_is_staff)
def students_view(request):
    """
    :param request:
    :return: renders student list with all department
    and semesters list.
    """
    all_students = Student.objects.select_related(
        'department', 'semester', 'ac_session').all()
    departments = Department.objects.select_related(
        'head').all()
    context = {'students': all_students,
               'departments': departments,
               }
    return render(request, 'students/students_list.html', context)


@user_passes_test(user_is_staff)
def students_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    students = Student.objects.select_related(
        'department', 'semester', 'ac_session').filter(department=dept_name)
    context = {'students': students, }
    return render(request, 'students/students_by_department.html', context)


class student_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    renders a student update form to update students details.
    """
    model = Student
    fields = ['photo', 'semester', 'mobile',
              'guardian_mobile', 'email']
    template_name = 'students/update_student.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:home')
        return redirect('account:login')

    def get_success_url(self):
        student_id = self.kwargs['pk']
        return reverse_lazy('students:student_details', kwargs={'pk': student_id})


class student_detail_view(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'students/student_details.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:home')
        return redirect('account:login')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = kwargs['object']
        pk = obj.id
        student = Student.objects.get(pk=pk)
        # get student object
        # for showing subjects in option form
        try:
            student_subject_qs = student.has_subjects()[0]
            student_subject_qs = student_subject_qs.subjects.all()
            context['subjects'] = student_subject_qs
        except IndexError:
            context['subjects'] = None
        # getting result objects
        semesters = range(1, student.semester.number + 1)
        context['semesters'] = semesters
        return context


@user_passes_test(user_is_staff)
def student_delete_view(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('students:all_student')
