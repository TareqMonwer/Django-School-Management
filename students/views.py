from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm


@login_required
def add_student_view(request):
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
    all_students = Student.objects.all()
    context = {'students': all_students}
    return render(request, 'students/students_list.html', context)


class student_update_view(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'students/update_student.html'

    def get_success_url(self):
        student_id = self.kwargs['pk']
        return reverse_lazy('students:student_details', kwargs={'pk': student_id})


class student_detail_view(DetailView):
    model = Student
    template_name = 'students/student_details.html'
