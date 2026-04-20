from django.contrib import admin
from .models import (
    Curriculum,
    CurriculumLevel,
    Stream,
    SubjectTemplate,
    CurriculumSubject,
)


class CurriculumLevelInline(admin.TabularInline):
    model = CurriculumLevel
    extra = 0
    ordering = ['level_number']


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'board', 'institute_type', 'is_active', 'display_order')
    list_filter = ('institute_type', 'is_active', 'board')
    search_fields = ('name', 'code')
    inlines = [CurriculumLevelInline]


@admin.register(CurriculumLevel)
class CurriculumLevelAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'level_number', 'name', 'semester_number', 'streams_applicable', 'display_order')
    list_filter = ('curriculum', 'streams_applicable')
    search_fields = ('name',)
    ordering = ('curriculum', 'level_number')


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'display_order')
    search_fields = ('name', 'code')


@admin.register(SubjectTemplate)
class SubjectTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'default_theory_marks', 'default_practical_marks', 'is_elective', 'display_order')
    list_filter = ('is_elective',)
    search_fields = ('name', 'code')


@admin.register(CurriculumSubject)
class CurriculumSubjectAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'level', 'stream', 'subject_template', 'is_compulsory', 'display_order')
    list_filter = ('curriculum', 'level', 'stream', 'is_compulsory')
    search_fields = ('subject_template__name', 'subject_template__code')
    autocomplete_fields = ('curriculum', 'level', 'stream', 'subject_template')
    ordering = ('curriculum', 'level', 'stream', 'display_order')
