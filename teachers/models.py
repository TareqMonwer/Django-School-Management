from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager


class Designation(TimeStampedModel):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Teacher(TimeStampedModel):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='teachers',
                              default='teacheravatar.jpg')
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    expertise = TaggableManager(blank=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['joining_date', 'name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.designation)
