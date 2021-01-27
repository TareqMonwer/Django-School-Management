from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.conf import settings


class User(AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('subscriber', 'Subscriber'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('editor', 'Editor'),
        ('academic_oficer', 'Academic Officer'),
        ('admin', 'Admin'),
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
    employee_or_student_id = models.CharField(
        max_length=10,
        blank=True, null=True
    )
    requested_role = models.CharField(
        choices=REQUESTED_ACCOUNT_TYPE_CHOICES,
        max_length=50,
        default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0]
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
