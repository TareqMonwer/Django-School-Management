from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_tools.models import Department, Semester, SemesterCombination
from result.models import Result, SubjectCombination, Subject
from .models import Student
from .forms import StudentForm


@login_required
def student_result_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        semester = request.POST.get('semester')
        student = Student.objects.get(roll=student_id)
        res_semester = Semester.objects.get(number=semester)
        results = Result.objects.filter(student=student, semester=res_semester)
        ctx = {
            'semester': res_semester,
            'results': results,
            'student': student,
        }
        return render(request, 'students/result.html', ctx)
    else:
        return render(request, 'students/result.html')


@login_required
def add_student_view(request):
    """
    :param request:
    :return: admission form to
    logged in user.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            return redirect('students:student_details', pk=pk)
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'students/addstudent.html', context)


@login_required
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
    semesters = SemesterCombination.objects.select_related(
        'department', 'semester', 'batch').all()
    context = {'students': all_students,
               'departments': departments,
               'semesters': semesters}
    return render(request, 'students/students_list.html', context)


@login_required
def students_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    students = Student.objects.select_related(
        'department', 'semester', 'ac_session').filter(department=dept_name)
    semesters = SemesterCombination.objects.select_related(
        'department', 'semester', 'batch').all()
    context = {'students': students,
               'semesters': semesters}
    return render(request, 'students/students_by_department.html', context)


class student_update_view(LoginRequiredMixin, UpdateView):
    """
    renders a student update form to update students details.
    """
    model = Student
    fields = ['photo', 'semester', 'mobile',
             'guardian_mobile', 'email']
    template_name = 'students/update_student.html'

    def get_success_url(self):
        student_id = self.kwargs['pk']
        return reverse_lazy('students:student_details', kwargs={'pk': student_id})


class student_detail_view(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_details.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = kwargs['object']
        pk = obj.id
        student = Student.objects.get(pk=pk)
        # get student object
        # for showing subjects in option form
        student_subject_qs = student.has_subjects()[0]
        student_subject_qs = student_subject_qs.subjects.all()
        context['subjects'] = student_subject_qs
        # getting result objects
        semesters = range(1, student.semester.number + 1)
        context['semesters'] = semesters
        return context


@login_required
def student_delete_view(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('students:all_student')


@login_required
def add_result_from_student_detail_view(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        subject = Subject.objects.get(subject_code=int(subject))
        marks = request.POST.get('marks')
        semester = student.semester
        try:
            result = Result(
                subject=subject,
                marks=marks,
                semester=semester,
                student=student)
            result.save()
        except IntegrityError as err:
            return HttpResponse('This result already recorded!')
        
        return redirect('students:student_details', pk=pk)
