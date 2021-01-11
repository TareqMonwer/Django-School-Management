from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from academics.models import Department
from students.models import Student
from teachers.models import Teacher
from .forms import UserRegistrationForm
from .models import CustomGroup, User


def user_is_staff(user):
    return user.is_staff


def profile_complete(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        employee_or_student_id = request.POST.get('employee_or_student_id')
        role = request.POST.get('role')
        email = request.POST.get('email')
        extra_note = request.POST.get('extra_note')

        user.email = email
        user.employee_or_student_id = employee_or_student_id
        user.requested_role = role
        user.approval_extra_note = extra_note
        user.approval_status = 'p'
        user.save()
        return redirect('account:profile_complete')

    return render(request, 'account/profile_complete.html')


@user_passes_test(user_is_staff, login_url='account:login')
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
    }
    return render(request, 'dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password1'])
            new_user.save()
            auth_user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            )
            if auth_user is not None:
                login(request, auth_user)
            if auth_user.is_staff:
                return redirect('account:dashboard')
            else:
                return redirect('account:profile_complete')
        else:
            return render(request, 'account/register.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'academics/accounts_list.html'
    context_object_name = 'accounts'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account:login')



class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomGroup
    template_name = 'academics/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account:login')


class UserRequestsListView(LoginRequiredMixin, ListView):
    queryset = User.objects.exclude(approval_status='a')
    template_name = 'account/user_requests.html'
    context_object_name = 'users'

user_requests_list = UserRequestsListView.as_view()