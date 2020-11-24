from django.contrib import admin
from .models import Student, AdmissionStudent, RegularStudent

admin.site.register(Student)
admin.site.register(AdmissionStudent)
admin.site.register(RegularStudent)
