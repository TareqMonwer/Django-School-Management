from django.contrib import admin
from .models import Student, AdmissionStudent, RegularStudent


class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


admin.site.register(Student)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
admin.site.register(RegularStudent)
