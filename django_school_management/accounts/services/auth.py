from django_school_management.accounts.constants import (
    ProfileApprovalStatusEnum,
    AccountTypesEnum,
)
from django_school_management.accounts.models import (
    CommonUserProfile,
    CustomGroup,
)
from django_school_management.accounts.request_context import (
    RequestUserContext,
)


def create_profile_for_approved_account(user):
    if user.approval_status == ProfileApprovalStatusEnum.approved.value:
        profile, created = CommonUserProfile.objects.get_or_create(user=user)
        return profile, created
    return None, None


def handle_superuser_creation(user):
    create_profile_for_approved_account(user)
    user.approval_status = ProfileApprovalStatusEnum.approved.value
    user.requested_role = AccountTypesEnum.admin.value
    user.save()


def assign_role_based_groups(user):
    already_assigned_to_group = user.groups.filter(
        name=user.requested_role
    ).exists()
    if (
        user.approval_status == ProfileApprovalStatusEnum.approved.value
        and not already_assigned_to_group
    ):
        group_creator = RequestUserContext.get_current_user()
        group, created = CustomGroup.objects.get_or_create(
            name=user.requested_role, group_creator=group_creator
        )
        user.groups.add(group)
