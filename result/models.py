from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings

from students.models import Student
from academics.models import Subject, Semester


class Exam(TimeStampedModel):
    EXAM_CHOICES = (
        ('Mid Term', 'm'),
        ('Final', 'f')
    )
    exam_name = models.CharField(
        max_length=1,
        choices=EXAM_CHOICES
    )
    exam_date = models.DateTimeField()


class Result(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    practical_marks = models.SmallIntegerField(
        blank=True,
        null=True
    )
    theory_marks = models.SmallIntegerField(
        blank=True,
        null=True
    )
    total_marks = models.SmallIntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.student} | {self.subject} | {self.total_marks}'
    
    def save(self, *args, **kwargs):
        if self.theory_marks and self.practical_marks:
            self.total_marks = self.practical_marks + self.theory_marks
        elif self.practical_marks and not self.theory_marks:
            self.total_marks = self.practical_marks
        else:
            self.total_marks = self.theory_marks
        super().save(*args, **kwargs)
