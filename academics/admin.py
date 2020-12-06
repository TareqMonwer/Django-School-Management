from django.contrib import admin
from .models import (AcademicSession,
                    Semester, Department,
                    Batch)



class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('year', 'created_by')


class BatchAdmin(admin.ModelAdmin):
    list_display = ('year', 'number')


admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Semester)
admin.site.register(Department)
