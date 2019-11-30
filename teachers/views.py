from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Teacher, Designation
from .forms import TeacherForm, TeacherDesignationForm


@login_required
def teachers_view(request):
    """
    :param request:
    :return: list of teachers to logged in user, login form instead.
    """
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teacher_list.html', context)


# THIS VIEW DUPLICATES QUERY
# AND RUNS 6 QUERIES
@login_required
def add_teacher_view(request):
    """
    :param request:
    :return: teacher add form
    """
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            return redirect('teachers:teacher_details', pk=pk)
    form = TeacherForm()
    context = {'form': form}
    return render(request, 'teachers/add_teacher.html', context)


@login_required
def teacher_detail_view(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher_detail.html', context)


class teacher_update_view(LoginRequiredMixin, UpdateView):
    model = Teacher
    fields = '__all__'
    template_name = 'teachers/update_teacher.html'

    def get_success_url(self):
        teacher_id = self.kwargs['pk']
        return reverse_lazy('teachers:teacher_details', kwargs={'pk': teacher_id})


@login_required
def teacher_delete_view(requset, pk):
    teacher = Teacher.objects.get(pk=pk)
    teacher.delete()
    return redirect('teachers:all_teacher')


def create_designation(request):
    if request.method == 'POST':
        form = TeacherDesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers:designations')
    else:
        form = TeacherDesignationForm()
    context = {'form': form}
    return render(request, 'teachers/designation_create.html', context)


class designation_list_view(LoginRequiredMixin, ListView):
    model = Designation
    template_name = 'teachers/designation_list.html'
