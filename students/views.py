from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from result.models import Result
from .models import Student
from .forms import StudentForm


@login_required
def student_result_view(request, student_id, semester):
    student = Student.objects.get(roll=student_id)
    res_semester = Semester.objects.get(number=semester)
    results = Result.objects.filter(student=student, semester=res_semester)
    ctx = {
        'semester': res_semester,
        'results': results,
        'student': student,
    }
    return render(request, 'students/result.html', ctx)


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
