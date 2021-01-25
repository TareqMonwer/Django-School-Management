from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe



class InstituteProfile(models.Model):
	name = models.CharField(max_length=255)
	date_of_estashment = models.DateField(blank=True, null=True)
	logo  = models.ImageField(upload_to='institute/')
	logo_small = models.ImageField(upload_to='institute/', blank=True, null=True)
	site_favicon = models.ImageField(upload_to='institute', blank=True, null=True)
	site_header = models.CharField(
		help_text='Will be displayed in SuperAdmin Dashboard',
		max_length=100,
		default='Django-School-Management'
	)
	site_title = models.CharField(
		help_text='Title of the application/site',
		max_length=100,
		default='Welcome to the Django-School-Management'
	)
	index_title = models.CharField(
		help_text='Will be displayed in SuperAdmin dashboard listing pages',
		max_length=100,
		default='Django-School-Management Admin'
	)
	active = models.BooleanField(default=False, unique=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.DO_NOTHING
	)

	def __str__(self):
		return self.name


class BaseWidget(TimeStampedModel):
	WIDGET_TYPE_CHOICES = (
		('text', 'Text Content'),
		('list', 'List Items'),
	)
	widget_type = models.CharField(
		max_length=10,
		choices=WIDGET_TYPE_CHOICES,
		default=WIDGET_TYPE_CHOICES[0][0]
	)
	widget_title = models.CharField(max_length=50)
	widget_number = models.PositiveSmallIntegerField(unique=True)

	class Meta:
		abstract = True


class TextWidget(BaseWidget):
	content = RichTextUploadingField(config_name='default')

	def __str__(self):
		return self.widget_title


class ListWidget(BaseWidget):
	pass

	def __str__(self):
		return self.widget_title


class WidgetListItem(TimeStampedModel):
	widget = models.ForeignKey(
		ListWidget,
		on_delete=models.CASCADE
	)
	text = models.CharField(max_length=150)
	link = models.URLField(
		max_length=255,
		blank=True, null=True
	)

	def __str__(self):
		return self.text

	def __html__(self):
		return mark_safe(
			'<a href="{0}">{1}</>'.format(self.link, self.text)
		)
