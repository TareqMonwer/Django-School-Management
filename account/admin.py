from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin

from .models import CustomGroup
from .forms import UserRegistrationForm, UserChangeForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserRegistrationForm
    fieldsets = (
        ("User", {"fields": ("account_type",)}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser"]

class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name', 'group_creator')

admin.site.register(CustomGroup, CustomGroupAdmin)