from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings

from students.models import Student
from academics.models import Subject, Semester, Department


class Exam(TimeStampedModel):
    EXAM_CHOICES = (
        ('m', 'Mid Term'),
        ('f', 'Final')
    )
    exam_name = models.CharField(
        max_length=1,
        choices=EXAM_CHOICES
    )
    exam_date = models.DateTimeField()

    def __str__(self):
        return f'{self.get_exam_name_display()} - \
            {self.exam_date.year}'


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
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE,
        blank=True, null=True
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

    class Meta:
        unique_together =  ('student', 'semester', 'subject')

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


class SubjectGroup(TimeStampedModel):
    """ Keep track of group of subjects that belongs to a
    department, semester
    """
    department = models.ForeignKey(
        Department,
        related_name='subjects',
        on_delete=models.DO_NOTHING
    )
    semester = models.ForeignKey(
        Semester,
        related_name='subjects',
        on_delete=models.CASCADE
    )
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f'{self.department} - {self.semester}'
    
    def get_subjects(self):
        return "\n".join([sg.subjects for sg in self.subjects.all()])
