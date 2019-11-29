from django.contrib import admin
from .models import (AcademicSession,
                     Semester, Department,
                     SemesterCombination)


admin.site.register(AcademicSession)
admin.site.register(Semester)
admin.site.register(Department)
admin.site.register(SemesterCombination)
