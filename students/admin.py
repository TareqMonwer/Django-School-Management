from django.contrib import admin
from .models import Student, AdmissionStudent, RegularStudent


class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created', 'city',
        'department_choice', 'admitted',
        'assigned_as_student'
    )
    list_editable = ('admitted', 'assigned_as_student')
    list_filter = (
        'paid', 'rejected', 'department_choice',
        'admitted', 'city',
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_student',
                    'ac_session',
                    'batch',
                    'temp_serial',
                    'temporary_id')


admin.site.register(Student, StudentAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
admin.site.register(RegularStudent)
