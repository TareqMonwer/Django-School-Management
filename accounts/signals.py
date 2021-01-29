from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CommonUserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if instance.approval_status == 'a':
        CommonUserProfile.objects.create(user=instance)