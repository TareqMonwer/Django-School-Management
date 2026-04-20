from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import model_help_texts
from .education_boards import BD_BOARDS, COUNTRY_BD


# Institute type determines terminology and flows (Department vs Group, counselling, etc.)
INSTITUTE_TYPE_POLYTECHNIC = 'polytechnic'
INSTITUTE_TYPE_SCHOOL = 'school'
INSTITUTE_TYPE_MADRASAH = 'madrasah'

INSTITUTE_TYPE_CHOICES = [
    (INSTITUTE_TYPE_SCHOOL, 'School (e.g. SSC/HSC)'),
    (INSTITUTE_TYPE_MADRASAH, 'Madrasah (e.g. Dakhil, Alim, Fazil)'),
    (INSTITUTE_TYPE_POLYTECHNIC, 'Polytechnic Institute'),
]

# Order for onboarding priority: school first, then madrasah, then polytechnic
INSTITUTE_TYPE_ONBOARDING_ORDER = [
    INSTITUTE_TYPE_SCHOOL,
    INSTITUTE_TYPE_MADRASAH,
    INSTITUTE_TYPE_POLYTECHNIC,
]


class EducationBoard(ExportModelOperationsMixin('education_board'), models.Model):
	"""Education boards per country for admission forms (e.g. BISE Dhaka)."""
	country = CountryField(db_index=True)
	name = models.CharField(max_length=120)
	code = models.CharField(max_length=30, blank=True, help_text='Short code for display')

	class Meta:
		ordering = ['country', 'name']
		unique_together = [('country', 'name')]

	def __str__(self):
		return self.name

	@classmethod
	def get_boards_for_country(cls, country_code):
		"""Return boards for a country. For BD ensures fixture data exists if empty."""
		if country_code is None:
			return cls.objects.none()
		# Normalize: CountryField may return Country object with .code
		code = getattr(country_code, 'code', country_code) or str(country_code) if country_code else None
		if not code:
			return cls.objects.none()
		qs = cls.objects.filter(country=code)
		if code == COUNTRY_BD and not qs.exists():
			for name, c in BD_BOARDS:
				cls.objects.get_or_create(country=code, name=name, defaults={'code': c})
			qs = cls.objects.filter(country=code)
		return qs


class InstituteProfile(ExportModelOperationsMixin('institute_profile'), models.Model):
	name = models.CharField(max_length=255)
	date_of_estashment = models.DateField(blank=True, null=True)
	country = CountryField(blank=True, null=True)
	logo = models.ImageField(upload_to='institute/')
	logo_small = models.ImageField(upload_to='institute/', blank=True, null=True)
	site_favicon = models.ImageField(upload_to='institute', blank=True, null=True)
	site_header = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SITEHEADER,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SITEHEADER_DEFAULT
	)
	site_title = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SITETITLE,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SITETITLE_DEFAULT
	)
	super_admin_index_title = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE_DEFAULT
	)
	motto = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	active = models.BooleanField(default=False, unique=True)
	onboarding_completed = models.BooleanField(default=False)
	# Institute type: school / madrasah use "Group"; polytechnic uses "Department" and has counselling.
	institute_type = models.CharField(
		max_length=20,
		choices=INSTITUTE_TYPE_CHOICES,
		blank=True,
		null=True,
		help_text='Determines terminology (Department vs Group) and admission/counselling flow.',
	)
	# For school/madrasah: one active session across all groups. For polytechnic: multiple sessions per dept (not set here).
	current_session = models.ForeignKey(
		'academics.AcademicSession',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='institutes_using_as_current',
		help_text='Single active academic session for school/madrasah. Leave blank for polytechnic.',
	)
	# Optional: default curriculum for this institute (e.g. Madrasah Ebtedayi). Used to suggest subjects/levels when creating groups and subject groups.
	curriculum = models.ForeignKey(
		'curriculum.Curriculum',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='institutes',
		help_text='Optional. Curriculum library this institute follows (e.g. Ebtedayi, Dakhil, HSC Science). Used to suggest subjects per class/group.',
	)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True
	)

	def __str__(self):
		return self.name

	@property
	def onboarding_step(self):
		"""Returns the next step the user should complete, or None if done."""
		if self.onboarding_completed:
			return None
		from django_school_management.academics.models import Department
		if not Department.objects.filter(institute=self).exists():
			return 2
		return 3

	def get_absolute_url(self):
		return reverse('institute:institute_detail', args=[self.pk])

	@property
	def is_polytechnic(self):
		return self.institute_type == INSTITUTE_TYPE_POLYTECHNIC

	@property
	def is_school_or_madrasah(self):
		return self.institute_type in (INSTITUTE_TYPE_SCHOOL, INSTITUTE_TYPE_MADRASAH)

	@property
	def department_label_plural(self):
		"""Plural for department_label: 'Groups' or 'Departments'."""
		if self.is_school_or_madrasah:
			return 'Groups'
		return 'Departments'

	@property
	def department_label(self):
		"""Display label for Department model: 'Group' for school/madrasah, 'Department' for polytechnic."""
		if self.is_school_or_madrasah:
			return 'Group'
		return 'Department'

	@property
	def semester_label(self):
		"""Display label for Semester: 'Class' for school/madrasah, 'Semester' for polytechnic."""
		if self.is_school_or_madrasah:
			return 'Class'
		return 'Semester'

	@property
	def semester_label_plural(self):
		"""Plural for semester_label: 'Classes' or 'Semesters'."""
		if self.is_school_or_madrasah:
			return 'Classes'
		return 'Semesters'


class City(ExportModelOperationsMixin('city'), TimeStampedModel):
	name = models.CharField(max_length=150)
	country = CountryField()
	code = models.CharField(
		max_length=10,
		help_text='Short code or district number (e.g. "13" for Dhaka)',
	)

	class Meta:
		verbose_name_plural = 'cities'
		ordering = ['name']
		unique_together = ['country', 'code']

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


class TextWidget(ExportModelOperationsMixin('text_widget'), BaseWidget):
	content = RichTextUploadingField(config_name='default')

	def __str__(self):
		return self.widget_title


class ListWidget(ExportModelOperationsMixin('list_widget'), BaseWidget):
	pass

	def __str__(self):
		return self.widget_title


class WidgetListItem(ExportModelOperationsMixin('widget_list_item'), TimeStampedModel):
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
