from django.contrib import admin
from .models import Teacher, Topic, Designation


admin.site.register(Topic)
admin.site.register(Designation)
admin.site.register(Teacher)