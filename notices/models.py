from datetime import date
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models


class Notice(TimeStampedModel):
    NOTICE_TYPES = (
        ('h', 'Holiday'),
        ('n', 'None')
    )
    title = models.CharField(max_length=255)
    notice_type = models.CharField(
        max_length=3,
        choices=NOTICE_TYPES,
        default='n'
    )
    file = models.FileField(
        upload_to='files/notices/',
        blank=True,
        null=True
    )
    content = RichTextUploadingField(config_name='default')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='published_notices',
        blank=True,
        null=True
    )
    notfiy_groups = models.ManyToManyField(
        'NotifyGroup',
        related_name='notfied_notices'
    )
    expires_at = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', ]
    
    @property
    def is_past_due(self):
        return date.today() > self.expires_at


class NotifyGroup(TimeStampedModel):
    group_name = models.CharField(max_length=55)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notify_groups'
    )

    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ['group_name', '-created']


class NoticeResponse(TimeStampedModel):
    notice = models.ForeignKey(
        Notice,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notice_responses'
    )

    def __str__(self):
        return f'{self.notice} - {self.responder}'
