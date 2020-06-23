from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from admin_tools.models import Department, Semester, AcademicSession


class Student(TimeStampedModel):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students',
                              default='studentavar.png')
    date_of_birth = models.DateField(blank=True, null=True)
    roll = models.CharField(max_length=6, unique=True)
    registration_number = models.CharField(max_length=6, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, default='1st')
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def has_subjects(self):
        from result.models import SubjectCombination
        return SubjectCombination.objects.filter(
            semester=self.semester, department=self.department
        )

    def __str__(self):
        return '{} ({}) semester {} dept.'.format(
            self.name, self.semester, self.department
        )

    class Meta:
        ordering = ['semester', 'roll', 'registration_number']
