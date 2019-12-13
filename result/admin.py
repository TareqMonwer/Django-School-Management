from django.contrib import admin

from .models import Result, Subject, SubjectCombination


admin.site.register(Result)
admin.site.register(Subject)
admin.site.register(SubjectCombination)
