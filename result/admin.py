from django.contrib import admin

from .models import Result, Exam


class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'semester', 'exam',
        'subject', 'theory_marks',
        'practical_marks', 'total_marks'
    )
    list_editable = ('total_marks', 'exam')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date')


admin.site.register(Result, ResutlAdmin)
admin.site.register(Exam, ExamAdmin)
