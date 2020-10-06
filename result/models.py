from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from students.models import Student, Semester
from teachers.models import Teacher
from academics.models import Department


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


class SubjectCombination(TimeStampedModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return '{} {}'.format(self.department, self.semester)


class Result(TimeStampedModel):
    marks = models.PositiveIntegerField()
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        blank=True, null=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        blank=True, null=True)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE,
        blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = ['subject', 'student']

    def grade(self):
        if 80 <= self.marks <= 100:
            return 'A+'
        elif 60 <= self.marks < 80:
            return 'A'
        elif 50 <= self.marks < 60:
            return ' A-'
        elif 40 <= self.marks < 50:
            return 'B'
        else:
            return 'F'

    def __str__(self):
        return "{} {} in {}".format(self.student.name, self.grade(),
                                    self.subject.name)
