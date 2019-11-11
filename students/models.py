from django.db import models
from teachers.models import Teacher


class Department(models.Model):
    name = models.CharField(max_length=255)
    head = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    establish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class AcademicSession(models.Model):
    year = models.CharField(max_length=9)

    def __str__(self):
        return str(self.year)


class Student(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    roll = models.CharField(max_length=6)
    registration_number = models.CharField(max_length=6)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=3, default='1st')
    ac_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, blank=True, null=True)
    mobile = models.CharField(max_length=11)
    guardian_mobile = models.CharField(max_length=11)
    email = models.EmailField()
    last_gpa = models.FloatField()

    def __str__(self):
        return '{} ({}) semester {} dept.'.format(
            self.name, self.semester, self.department
        )


