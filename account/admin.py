from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

from .models import CustomGroup



class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name', 'group_creator')


admin.site.register(CustomGroup, CustomGroupAdmin)