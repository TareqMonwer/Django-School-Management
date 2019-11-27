from django.db import models

from teachers.models import Teacher
from students.models import Student, Semester


class Subject(models.Model):
    name = models.CharField(max_length=50)
    subject_code = models.PositiveIntegerField()
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                   blank=True, null=True)
    theory_marks = models.PositiveIntegerField(blank=True, null=True)
    practical_marks = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.subject_code)


class Result(models.Model):
    marks = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,
                                 blank=True, null=True)

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
