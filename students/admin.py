from django.contrib import admin
from .models import (Department,
                     Student,
                     AcademicSession,
                     Semester)


admin.site.register(Department)
admin.site.register(Student)
admin.site.register(AcademicSession)
admin.site.register(Semester)