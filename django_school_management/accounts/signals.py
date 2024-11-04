from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from django_school_management.accounts.request_context import RequestUserContext
from django_school_management.accounts.services.auth import handle_superuser_creation, \
    create_profile_for_approved_account, assign_role_based_groups


User = get_user_model()

@receiver(user_logged_in)
def set_user_on_login(sender, request, user, **kwargs):
    RequestUserContext.set_current_user(user)

@receiver(user_logged_out)
def clear_user_on_logout(sender, request, user, **kwargs):
    RequestUserContext.clear_current_user()


@receiver(post_save, sender=get_user_model())
def assign_all_permissions_to_superuser(sender, instance, created, **kwargs):
    user = User.objects.get(id=instance.id)
    user_profile = getattr(user, 'profile', None)

    if instance.is_superuser and not user_profile:
        handle_superuser_creation(user)
    elif created and not user_profile:
        create_profile_for_approved_account(user)

    assign_role_based_groups(user)
