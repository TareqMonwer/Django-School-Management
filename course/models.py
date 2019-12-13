from django.db import models
from datetime import datetime

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    initial = models.CharField(max_length=255)


class Section(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)


class CourseAttendance(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    total_attendance = models.IntegerField()
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
