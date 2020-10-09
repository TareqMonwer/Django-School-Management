from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from academics.views import user_is_staff
from .models import Teacher, Designation
from .forms import TeacherForm, TeacherDesignationForm


@user_passes_test(user_is_staff)
def teachers_view(request):
    """
    :param request:
    :return: list of teachers to logged in user, login form instead.
    """
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teacher_list.html', context)


# TODO: Reduce duplicate queries.
@login_required
def add_teacher_view(request):
    """
    :param request:
    :return: teacher add form
    """
    if request.user.has_perm('create_teacher'):
        if request.method == 'POST':
            form = TeacherForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                pk = form.instance.pk
                return redirect('teachers:all_teacher')
        form = TeacherForm()
        context = {'form': form}
        return render(request, 'teachers/add_teacher.html', context)
    else:
        return render(request, 'admin_tools/permission_required.html')


@user_passes_test(user_is_staff)
def teacher_detail_view(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher_detail.html', context)


class teacher_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Teacher
    fields = '__all__'
    template_name = 'teachers/update_teacher.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:home')
        return redirect('account:login')

    def get_success_url(self):
        teacher_id = self.kwargs['pk']
        return reverse_lazy('teachers:teacher_details', kwargs={'pk': teacher_id})


@user_passes_test(user_is_staff)
def teacher_delete_view(requset, pk):
    teacher = Teacher.objects.get(pk=pk)
    teacher.delete()
    return redirect('teachers:all_teacher')


@user_passes_test(user_is_staff)
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


class designation_list_view(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Designation
    template_name = 'teachers/designation_list.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:home')
        return redirect('account:login')
