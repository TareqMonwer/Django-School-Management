from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.conf import settings


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('s', 'Subscriber'),
        ('s', 'Student'),
        ('t', 'Teacher'),
        ('e', 'Editor'),
        ('c', 'Academic Officer'),
        ('a', 'Admin'),
    )
    account_approved = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )
    account_type = models.CharField(
        max_length=2,
        choices=ACCOUNT_TYPE_CHOICES,
        default=ACCOUNT_TYPE_CHOICES[0]
    )   # default will be general user who have zero perms in the app.


class CustomGroup(Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    
    def display_group(self):
        return f'{self.name} created by {self.group_creator}'
