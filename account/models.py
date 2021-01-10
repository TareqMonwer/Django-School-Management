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
    APPROVAL_CHOICES = (
        ('n', 'Not Requested For Approval'),
        ('p', 'Approval Application on Pending'),
        ('d', 'Approval Request Declined'),
        ('a', 'Verified')
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_CHOICES[0][0],
    )
    account_type = models.CharField(
        max_length=2,
        choices=ACCOUNT_TYPE_CHOICES,
        default=ACCOUNT_TYPE_CHOICES[0][0]
    )  # default will be general user who have zero perms in the app.
    employee_or_student_id = models.CharField(
        max_length=10,
        blank=True, null=True
    )
    requested_role = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    approval_extra_note = models.TextField(
        blank=True, null=True
    )


class CustomGroup(Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    
    def display_group(self):
        return f'{self.name} created by {self.group_creator}'
