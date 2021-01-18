from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Teacher, Designation
from .forms import TeacherForm, TeacherDesignationForm
from permission_handlers.administrative import (
    user_editor_admin_or_su,
    user_is_admin_or_su,
    user_is_teacher_or_administrative,
)
from permission_handlers.basic import user_is_verified


@user_passes_test(user_is_teacher_or_administrative)
def teachers_view(request):
    """
    :param request:
    :return: list of teachers to logged in user, login form instead.
    """
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teacher_list.html', context)


# TODO: Reduce duplicate queries.
@user_passes_test(user_is_admin_or_su)
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


@user_passes_test(user_is_verified)
def teacher_detail_view(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher_detail.html', context)


class teacher_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Teacher
    fields = '__all__'
    template_name = 'teachers/update_teacher.html'

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')

    def get_success_url(self):
        teacher_id = self.kwargs['pk']
        return reverse_lazy('teachers:teacher_details', kwargs={'pk': teacher_id})


@user_passes_test(user_is_admin_or_su)
def teacher_delete_view(requset, pk):
    teacher = Teacher.objects.get(pk=pk)
    teacher.delete()
    return redirect('teachers:all_teacher')


@user_passes_test(user_is_admin_or_su)
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
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')
