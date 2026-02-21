from django.contrib.auth.models import Group

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


def _get_or_create_custom_group(role_name, creator):
    """Safely get or create a CustomGroup, handling the case where a base
    Group already exists (e.g. from seed data) without a CustomGroup child row."""
    try:
        return CustomGroup.objects.get(name=role_name)
    except CustomGroup.DoesNotExist:
        pass

    try:
        base_group = Group.objects.get(name=role_name)
        custom = CustomGroup(group_ptr=base_group, group_creator=creator)
        custom.save_base(raw=True)
        return CustomGroup.objects.get(pk=base_group.pk)
    except Group.DoesNotExist:
        return CustomGroup.objects.create(
            name=role_name,
            group_creator=creator,
        )


def assign_role_based_groups(user):
    already_assigned_to_group = user.groups.filter(
        name=user.requested_role
    ).exists()
    if (
        user.approval_status == ProfileApprovalStatusEnum.approved.value
        and not already_assigned_to_group
    ):
        group_creator = RequestUserContext.get_current_user()
        group = _get_or_create_custom_group(user.requested_role, group_creator)
        user.groups.add(group)
