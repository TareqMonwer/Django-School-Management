from django.contrib import admin

from .models import Result


class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'semester',
        'subject', 'theory_marks',
        'practical_marks', 'total_marks'
    )
    list_editable = ('total_marks',)


admin.site.register(Result, ResutlAdmin)
