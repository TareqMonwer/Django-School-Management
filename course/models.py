from django.db import models
from datetime import datetime
from teachers.models import Teacher
from students.models import Student

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    initial = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class CourseAttendance(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    course = models.ManyToManyField(Course)
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)

    def __int__(self):
        return self.id


class CourseAssignToTeacher(models.Model):
    course = models.ManyToManyField(Course)
    teacher = models.ManyToManyField(Teacher)

    def __int__(self):
        return self.id


class CourseAssignToStudent(models.Model):
    course = models.ManyToManyField(Course)
    student = models.ManyToManyField(Student)

    def __int__(self):
        return self.id
