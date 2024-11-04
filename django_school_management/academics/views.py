import csv, io

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .constants import AcademicsURLConstants
from .models import (Semester, Department,
    AcademicSession, Subject)
from .forms import SemesterForm, DepartmentForm, AcademicSessionForm, SubjectForm
from permission_handlers.administrative import (
    user_is_admin_su_editor_or_ac_officer,
    user_editor_admin_or_su,
    user_is_teacher_or_administrative,
)
from permission_handlers.basic import user_is_verified
from ..mixins.created_by import CreatedByMixin


@user_passes_test(user_is_admin_su_editor_or_ac_officer)
def semesters(request):
    """
    Shows semester list and
    contains semester create form
    """
    # TODO: Allow multiple semester creation together. (1,3,4,5) like this format.
    all_sems = Semester.objects.all()
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semster = form.save(commit=False)
            semster.created_by = request.user
            semster.save()
            return redirect(AcademicsURLConstants.all_semester)
    form = SemesterForm()
    ctx = {
        'all_sems': all_sems,
        'form': form,
    }
    return render(request, 'academics/all_semester.html', ctx)


@user_passes_test(user_is_admin_su_editor_or_ac_officer)
def academic_session(request):
    """
    Responsible for academic session list view
    and academic session create view.
    """
    if request.method == 'POST':
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            ac_session = form.save(commit=False)
            ac_session.created_by = request.user
            ac_session.save()
            return redirect(AcademicsURLConstants.academic_sessions)
    else:
        form = AcademicSessionForm()
    all_academic_session = AcademicSession.objects.all()
    ctx = {
        'form': form,
        'academic_sessions': all_academic_session,
    }
    return render(request, 'academics/academic_sessions.html', ctx)


@user_passes_test(user_is_verified)
def departments(request):
    """
    Responsible for department list view
    and department create view.
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.created_by = request.user
            dept.save()
            return redirect(AcademicsURLConstants.departments)
    else:
        form = DepartmentForm()
    all_department = Department.objects.all()
    ctx = {
        'form': form,
        'departments': all_department,
    }
    return render(request, 'academics/departments.html', ctx)


@user_passes_test(user_editor_admin_or_su)
def delete_semester(request, pk):
    obj = get_object_or_404(Semester, pk=pk)
    obj.delete()
    return redirect(AcademicsURLConstants.all_semester)


class UpdateDepartment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/update_department.html'
    success_url = reverse_lazy(AcademicsURLConstants.departments)

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

    def form_valid(self, form):
        return super().form_valid(form)


@user_passes_test(user_editor_admin_or_su)
def delete_department(request, pk):
    obj = get_object_or_404(Department, pk=pk)
    obj.delete()
    return redirect(AcademicsURLConstants.departments)


@user_passes_test(user_is_teacher_or_administrative)
def upload_subjects_csv(request):
    template = 'result/add_subject_csv.html'
    prompt = {
        'order': 'Subject name, Subject Code'
    }
    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please, upload a CSV file.')
    try:
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        # TODO: upload data for foreignkey also, and
        # create object for foreignkey if no data found.
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Subject.objects.update_or_create(
                name=column[0],
                subject_code=column[1]
            )
    except:
        pass
    context = {}
    return render(request, template, context)


class CreateDepartmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView, CreatedByMixin):
    form_class = DepartmentForm
    success_url = reverse_lazy(AcademicsURLConstants.departments)
    template_name = 'academics/create_department.html'

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

create_department = CreateDepartmentView.as_view()


class CreateSemesterView(LoginRequiredMixin, UserPassesTestMixin, CreateView, CreatedByMixin):
    form_class = SemesterForm
    success_url = reverse_lazy(AcademicsURLConstants.all_semester)
    template_name = 'academics/create_semester.html'

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

create_semester = CreateSemesterView.as_view()


class CreateAcademicSession(LoginRequiredMixin, UserPassesTestMixin, CreateView, CreatedByMixin):
    form_class = AcademicSessionForm
    success_url = reverse_lazy(AcademicsURLConstants.academic_sessions)
    template_name = 'academics/create_academic_semester.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

create_academic_semester = CreateAcademicSession.as_view()


class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'academics/subject_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

subject_list = SubjectListView.as_view()


class CreateSubjectView(LoginRequiredMixin, UserPassesTestMixin, CreateView, CreatedByMixin):
    form_class = SubjectForm
    template_name = 'academics/create_subject.html'
    success_url = reverse_lazy(AcademicsURLConstants.subject_list)

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

create_subject = CreateSubjectView.as_view()
