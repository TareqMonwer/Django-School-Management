"""
Handling permissions for users who are assigned 
for basic level actions in the project. (view few data, modify some of their data etc).
UserTypes: Student, Teacher
"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def permission_error(request):
    return HttpResponse('You don\'t have right permissio to access this page.')

def user_is_verified(user):
    return user.approval_status == 'a' if user.is_authenticated else False

def user_is_student(user):
    return user_is_verified(user) and user.requested_role == 'student' \
        if user.is_authenticated else False

def user_is_teacher(user):
    return user_is_verified(user) and user.requested_role == 'teacher' \
        if user.is_authenticated else False
