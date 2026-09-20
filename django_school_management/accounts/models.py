from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from django_prometheus.models import ExportModelOperationsMixin

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import reverse


class User(ExportModelOperationsMixin('user'), AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('subscriber', 'Subscriber'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('editor', 'Editor'),
        ('academic_officer', 'Academic Officer'),
        ('admin', 'Admin'),
    )
    APPROVAL_CHOICES = (
        ('n', 'Not Requested For Approval'),
        ('p', 'Approval Application is Pending'),
        ('d', 'Approval Request Declined'),
        ('a', 'Verified')
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_CHOICES,
        default='n',
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
    institute = models.ForeignKey(
        'institute.InstituteProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users',
    )

    def get_author_url(self):
        return reverse(
            'articles:author_profile',
            args=[self.username,])


class CustomGroup(ExportModelOperationsMixin('custom_group'), Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def display_group(self):
        return f'{self.name} created by {self.group_creator}'


class CommonUserProfile(ExportModelOperationsMixin('common_user_profile'), models.Model):
    """Core details of user profile created only after account verification by institute."""
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.SET_NULL,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile-pictures',
        blank=True,
        null=True
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    summary = RichTextUploadingField(
        blank=True,
        null=True
    )
    country = CountryField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user}\'s profile'
