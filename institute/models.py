from django.db import models
from django.conf import settings



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