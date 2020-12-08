from django.contrib import admin
from .models import Student, AdmissionStudent, RegularStudent


class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_student',
                    'ac_session',
                    'batch',
                    'temp_serial',)


admin.site.register(Student, StudentAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
admin.site.register(RegularStudent)
