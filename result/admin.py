from django.contrib import admin

from .models import Result, Exam, SubjectGroup


class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'semester', 'exam',
        'subject', 'theory_marks',
        'practical_marks', 'total_marks'
    )
    list_editable = ('total_marks', 'exam')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date')


class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('department', 'semester', 'get_subjects')


admin.site.register(Result, ResutlAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(SubjectGroup, SubjectGroupAdmin)
