from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import reverse


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

    def get_author_url(self):
        return reverse(
            'articles:author_profile',
            args=[self.username,])


class CustomGroup(Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def display_group(self):
        return f'{self.name} created by {self.group_creator}'


class SocialLink(models.Model):
    user_profile = models.ForeignKey(
        'CommonUserProfile',
        on_delete=models.CASCADE
    )
    media_name = models.CharField(
        max_length=50
    )
    url = models.URLField()

    def __str__(self):
        return self.media_name


class CommonUserProfile(models.Model):
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
    cover_picture = models.ImageField(
        upload_to='cover-pictures',
        blank=True,
        null=True
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    show_headline_in_bio = models.BooleanField(
        help_text='I want to use this as my bio',
        default=False
    )
    summary = RichTextUploadingField(
        help_text='Your Profile Summary',
        blank=True,
        null=True
    )
    country = CountryField(
        blank=True,
        null=True
    )
    social_links = models.ManyToManyField(
        SocialLink,
        related_name='social_links',
        blank=True
    )

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user}\'s profile'
