from datetime import date
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.urls import reverse


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
    content = RichTextUploadingField(
        config_name='default',
        blank=True,
        null=True
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='published_notices',
        blank=True,
        null=True
    )
    notfiy_groups = models.ManyToManyField(
        'NotifyGroup',
        related_name='notfied_notices',
        blank=True
    )
    expires_at = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', ]
    
    @property
    def is_past_due(self):
        return date.today() > self.expires_at
    
    @property
    def notice_file_type(self):
        if self.file:
            file_type = self.file.name.split('.')[-1].lower()
            if file_type in ['jpg', 'jpeg', 'png']:
                return 'img'
            if file_type == 'pdf':
                return 'pdf'
        return None
    
    def get_absolute_url(self):
        return reverse('notices:notice_detail', kwargs={'pk': self.pk})


class NoticeDocument(TimeStampedModel):
    notice = models.ForeignKey(
        Notice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents'
    )
    file = models.FileField(
        'Notice PDF Document',
        upload_to='files/notices/'
    )

    def __str__(self):
        return self.notice.title


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
