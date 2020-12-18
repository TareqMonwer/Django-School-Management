from django.contrib import admin
from .models import Student, AdmissionStudent, RegularStudent


class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'city', 'department_choice')
    list_filter = (
        'paid', 'rejected', 'department_choice',
        'admitted', 'city',
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_student',
                    'ac_session',
                    'batch',
                    'temp_serial',
                    'get_student_serial')

    def get_student_serial(self, obj):
        return obj.student_serial.get_serial()
    get_student_serial.short_description = 'Student ID'
    get_student_serial.admin_order_field = 'student_serial.get_serial'


admin.site.register(Student, StudentAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
admin.site.register(RegularStudent)
