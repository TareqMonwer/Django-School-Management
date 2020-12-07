from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

from teachers.models import Teacher
from students.models import RegularStudent
from academics.models import Batch


class Department(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField('Department Short Form', 
        max_length=5)
    code = models.PositiveIntegerField()
    head = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, blank=True, null=True)
    current_batch = models.ForeignKey(Batch, on_delete=models.CASCADE,
                    blank=True, null=True, related_name='current_batches')
    batches = models.ManyToManyField(Batch, blank=True, null=True)
    establish_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def dept_code(self):
        if not self.code:
            return ""
        return self.code

    def __str__(self):
        return str(self.name)


class AcademicSession(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return '{} - {}'.format(self.year, self.year + 1)


class Semester(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True)
    guide = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['number', ]

    def __str__(self):
        if self.number == 1:
            return '1st'
        if self.number == 2:
            return '2nd'
        if self.number == 3:
            return '3rd'
        if 3 < self.number <= 12:
            return '%sth' % self.number


class Subject(TimeStampedModel):
    name = models.CharField(max_length=50)
    subject_code = models.PositiveIntegerField(unique=True)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                    blank=True, null=True)
    theory_marks = models.PositiveIntegerField(blank=True, null=True)
    practical_marks = models.PositiveIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.subject_code)


class Batch(TimeStampedModel):
    year = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    number = models.PositiveIntegerField('Batch Number')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f'{self.department.name} Batch {self.number} ({self.year})'

    @classmethod
    def get_current_batch(year):
        Batch.objects.find(year=year)


class TempSerialID(TimeStampedModel):
    student = models.ForeignKey(RegularStudent, on_delete=models.CASCADE)
    serial = models.CharField(max_length=50, blank=True)

    def get_serial(self):
        # Get current year last two digit
        yf = self.student.created.date().year[-2:]
        # TODO: Get current batch of student's department
        bn = self.student.department.get_current_batch()
        # Get department code
        dc = self.student.department.code
        # Get admission serial of student by department
        syl = self.student.serial_key

        # return something like: 21-15-666-15
        return f'{yf}-{bn}-{dc}-{syl}'