from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CommonUserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """ Create a profile for the verfiied user if a profile 
    already doesn't belong to the user.
    """
    if instance.approval_status == 'a':
        try:
            profile = instance.profile
        except CommonUserProfile.DoesNotExist:
            CommonUserProfile.objects.create(user=instance)
