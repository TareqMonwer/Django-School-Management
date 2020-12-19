from django.contrib import admin

from .models import Result


class ResutlAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'subject', 'total_marks')


admin.site.register(Result, ResutlAdmin)
