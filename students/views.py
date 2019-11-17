from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Student, Semester, AcademicSession, Department
from .forms import StudentForm, SemesterForm, AcademicSessionForm, DepartmentForm


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
    :return: list of students to logged in user, login form instead.
    """
    all_students = Student.objects.all()
    context = {'students': all_students}
    return render(request, 'students/students_list.html', context)


class student_update_view(LoginRequiredMixin, UpdateView):
    """
    renders a student update form to update students details.
    """
    model = Student
    fields = '__all__'
    template_name = 'students/update_student.html'

    def get_success_url(self):
        student_id = self.kwargs['pk']
        return reverse_lazy('students:student_details', kwargs={'pk': student_id})


class student_detail_view(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_details.html'


@login_required
def student_delete_view(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('students:all_student')


@login_required
def semesters(request):
    all_sems = Semester.objects.all()
    return render(request, 'students/misc/all_semester.html', {'all_sems': all_sems})


@login_required
def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:all_semester')
    form = SemesterForm()
    return render(request, 'students/misc/add_semester.html', {'form': form})


@login_required
def delete_semester(request, pk):
    pass


@login_required
def add_academic_session(request):
    pass


@login_required
def add_department(request):
    pass

