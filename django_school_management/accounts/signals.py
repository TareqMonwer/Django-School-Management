from Tools.demo.mcast import sender
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import ProfileApprovalStatusEnum, AccountTypesEnum
from .models import CommonUserProfile


User = get_user_model()

def create_profile_for_approved_account(user):
    if user.approval_status == ProfileApprovalStatusEnum.approved.value:
        profile, created = CommonUserProfile.objects.get_or_create(user=user)
        return profile, created
    return None, None


@receiver(post_save, sender=get_user_model())
def assign_all_permissions_to_superuser(sender, instance, created, **kwargs):
    user = User.objects.get(id=instance.id)
    user_profile = getattr(user, 'profile', None)

    if instance.is_superuser and not user_profile:
        create_profile_for_approved_account(user)
        user.approval_status = ProfileApprovalStatusEnum.approved.value
        user.requested_role = AccountTypesEnum.admin.value
        user.save()
    elif created and not user_profile:
        create_profile_for_approved_account(user)
