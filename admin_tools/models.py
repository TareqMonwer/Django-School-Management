from django.db import models
from teachers.models import Teacher


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.PositiveIntegerField(blank=True, null=True)
    head = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, blank=True, null=True)
    establish_date = models.DateField(auto_now_add=True)

    def dept_code(self):
        if not self.code:
            return ""
        return self.code

    def __str__(self):
        return str(self.name)


class AcademicSession(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return '{} - {}'.format(self.year, self.year + 1)


class Semester(models.Model):
    number = models.PositiveIntegerField(unique=True)
    guide = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=None, null=True, blank=True)

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
