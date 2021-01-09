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


def home(request):
    return HttpResponse("Welcome Home")


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
            print(user_form.cleaned_data)
            return HttpResponse('aaaaa')
            # new_user = user_form.save(commit=False)
            # new_user.set_password(
            #     user_form.cleaned_data['password'])
            # new_user.save()
            # auth_user = authenticate(username=user_form.cleaned_data['username'],
            #                          password=user_form.cleaned_data['password'])
            # if auth_user is not None:
            #     login(request, auth_user)
            # if auth_user.is_staff:
            #     return redirect('account:dashboard')
            # else:
            #     return redirect('account:home')
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
            return redirect('account:home')
        return redirect('account:login')



class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomGroup
    template_name = 'academics/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:home')
        return redirect('account:login')
