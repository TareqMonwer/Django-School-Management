"""
Handling permissions for administrators who are assigned to handle everything.
Admins have direct role after superuser.
UserTypes: Admin, SuperAdmin
"""
from .editor import (
    user_is_editor,
    user_is_academic_officer,
    user_is_editor_or_ac_officer
)
from .basic import user_is_verified, user_is_teacher, user_is_student

def user_is_admin(user):
    return user_is_verified(user) and user.requested_role == 'admin'

def user_is_superuser(user):
    return user_is_admin(user) and user.is_superuser

def user_is_admin_or_su(user):
    return user_is_admin(user) or user_is_superuser(user)

def user_is_admin_su_or_ac_officer(user):
    return user_is_admin_or_su(user) or user_is_academic_officer(user)

def user_editor_admin_or_su(user):
    return user_is_admin_or_su(user) or user_is_editor(user)

def user_is_admin_su_editor_or_ac_officer(user):
    return user_is_admin_or_su(user) or user_is_editor_or_ac_officer(user)

def user_is_teacher_or_administrative(user):
    return user_is_admin_su_editor_or_ac_officer(user) or user_is_teacher(user)

def user_is_student_or_administrative(user):
    return user_is_admin_su_editor_or_ac_officer(user) or user_is_student(user)
