"""
Handling permissions for users who are assigned
for basic level actions in the project. (view few data, modify some of their data etc).
UserTypes: Student, Teacher
"""

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django_school_management.accounts.constants import (
    AccountTypesEnum,
    ProfileApprovalStatusEnum,
)
from django_school_management.accounts.models import User


@login_required
def permission_error(request):
    return HttpResponse("You don't have right permission to access this page.")


def user_is_verified(user):
    return (
        user.approval_status == ProfileApprovalStatusEnum.approved.value
        if user.is_authenticated
        else False
    )


def user_is_student(user):
    return (
        user_is_verified(user)
        and user.requested_role == AccountTypesEnum.student.value
        if user.is_authenticated
        else False
    )


def user_is_teacher(user):
    return (
        user_is_verified(user)
        and user.requested_role == AccountTypesEnum.teacher.value
        if user.is_authenticated
        else False
    )


def can_access_dashboard(user: User):
    restricted_roles = [AccountTypesEnum.subscriber.value]
    if user.requested_role in restricted_roles:
        return False
    if user.approval_status != ProfileApprovalStatusEnum.approved.value:
        return False
    return True
