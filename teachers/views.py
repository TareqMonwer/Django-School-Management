from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

from .models import Teacher
from .forms import TeacherForm


@login_required
def teachers_view(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teacher_list.html', context)


@login_required
def add_teacher_view(request):
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


class teacher_update_view(UpdateView):
    model = Teacher
    fields = '__all__'
    template_name = 'teachers/update_teacher.html'

    def get_success_url(self):
        teacher_id = self.kwargs['pk']
        return reverse_lazy('teachers:teacher_details', kwargs={'pk': teacher_id})
