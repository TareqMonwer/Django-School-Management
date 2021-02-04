from rolepermissions.roles import assign_role
from rolepermissions.admin import RolePermissionsUserAdminMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin

from .models import CustomGroup, CommonUserProfile, SocialLink
from .forms import UserRegistrationForm, UserChangeForm

User = get_user_model()


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(RolePermissionsUserAdminMixin, ImportExportModelAdmin, auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserRegistrationForm
    fieldsets = (
        ("User", {"fields": ("approval_status", "requested_role")}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser", "approval_status", "requested_role"]
    list_editable = ["approval_status",]
    search_fields = ["approval_status", "requested_role"]
    resource_class = UserResource

    # TODO: Assign users to requested group
    # def save_model(self, request, obj, form, change): 
    #     instance = form.save(commit=False)
    #     requested_role = request.POST.get('requested_role')
    #     assign_role(obj, requested_role)
    #     instance.save()
    #     return instance


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = CommonUserProfile


class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserProfileResource


class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name', 'group_creator')


admin.site.register(CommonUserProfile, UserProfileAdmin)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(User, UserAdmin)
