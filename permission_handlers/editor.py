"""
Handling permissions for editors who are assigned to perform few important actions.
e.g. create article, moderate user profiles, department and other academic moderations.
UserTypes: Editor, AcademicOfficer
"""
from .basic import user_is_verified

def user_is_editor(user):
    return user_is_verified(user) and user.requested_role == 'editor'


def user_is_academic_officer(user):
    return user_is_verified(user) and user.requested_role == 'academic_oficer'


def user_is_editor_or_ac_officer(user):
    return user_is_editor(user) or user_is_academic_officer(user)