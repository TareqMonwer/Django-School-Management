from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import (
    InstituteProfile, TextWidget,
    ListWidget, WidgetListItem
)


class InstituteProfileResource(resources.ModelResource):
    class Meta:
        model = InstituteProfile


class InstituteProfileAdmin(ImportExportModelAdmin):
    resource_class = InstituteProfileResource


class WidgetListItemResource(resources.ModelResource):
    class Meta:
        model = WidgetListItem


class WidgetListItemInline(admin.TabularInline):
    model = WidgetListItem


class ListWidgetResource(resources.ModelResource):
    class Meta:
        model = ListWidget


class ListWidgetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [
            WidgetListItemInline,
    ]
    resource_class = ListWidgetResource


class TextWidgetResource(resources.ModelResource):
    class Meta:
        model = TextWidget


class TextWidgetAdmin(ImportExportModelAdmin):
    resource_class = TextWidgetResource


admin.site.register(InstituteProfile, InstituteProfileAdmin)
admin.site.register(TextWidget, TextWidgetAdmin)
admin.site.register(ListWidget, ListWidgetAdmin)
admin.site.register(WidgetListItem)
