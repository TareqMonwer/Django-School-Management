from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from teachers.models import Teacher
from students.models import Student


class Course(TimeStampedModel):
    title = models.CharField(max_length=255)
    initial = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.title


class Section(TimeStampedModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class CourseAttendance(TimeStampedModel):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    course = models.ManyToManyField(Course)
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)

    def __int__(self):
        return self.id


class CourseAssignToTeacher(TimeStampedModel):
    course = models.ManyToManyField(Course)
    teacher = models.ManyToManyField(Teacher)
    assign_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __int__(self):
        return self.id


class CourseAssignToStudent(TimeStampedModel):
    course = models.ManyToManyField(Course)
    student = models.ManyToManyField(Student)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    def __int__(self):
        return self.id


class DailyAttendance(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    is_present = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
