from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from rolepermissions.roles import assign_role

from .models import Semester, Department, AcademicSession
from .forms import SemesterForm, DepartmentForm, AcademicSessionForm
from account.forms import UserRegistrationForm


def user_is_staff(user):
    return user.is_staff

@login_required
def add_user_view(request):
    if request.user.has_perm('create_stuff'):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                role = request.POST.get('user_role')
                if role == 'admin':
                    user = user_form.save()
                    assign_role(user, 'admin')
                    return redirect('academics:all_accounts')
                elif role == 'stuff':
                    user = user_form.save()
                    assign_role(user, 'stuff')
                    return redirect('academics:all_accounts')
            else:
                return render(request, 'academics/add_user.html')
        else:
            user_form = UserRegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, 'academics/add_user.html', context)
    else:
        return render(request, 'academics/permission_required.html')


@user_passes_test(user_is_staff)
def semesters(request):
    '''
    Shows semester list and 
    contains semester create form
    '''
    all_sems = Semester.objects.all()
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:all_semester')
    form = SemesterForm()
    ctx = {
        'all_sems': all_sems,
        'form': form,
    }
    return render(request, 'academics/all_semester.html', ctx)


@user_passes_test(user_is_staff)
def academic_session(request):
    '''
    Responsible for academic session list view
    and academic session create view.
    '''
    if request.method == 'POST':
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:academic_sessions')
    else:
        form = AcademicSessionForm()
    all_academic_session = AcademicSession.objects.all()
    ctx = {
        'form': form,
        'academic_sessions': all_academic_session,
    }
    return render(request, 'academics/academic_sessions.html', ctx)


@user_passes_test(user_is_staff)
def departments(request):
    '''
    Responsible for department list view
    and department create view.
    '''
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:departments')
    else:
        form = DepartmentForm()
    all_department = Department.objects.all()
    ctx = {
        'form': form,
        'departments': all_department,
    }
    return render(request, 'academics/departments.html', ctx)


@user_passes_test(user_is_staff)
def delete_semester(request, pk):
    pass
