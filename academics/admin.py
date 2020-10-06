from django.contrib import admin
from .models import (AcademicSession,
                    Semester, Department)


admin.site.register(AcademicSession)
admin.site.register(Semester)
admin.site.register(Department)
