from django.contrib import admin

from .models import (
    InstituteProfile, TextWidget,
    ListWidget, WidgetListItem
)


class WidgetListItemInline(admin.TabularInline):
    model = WidgetListItem


class ListWidgetAdmin(admin.ModelAdmin):
    inlines = [
            WidgetListItemInline,
    ]


admin.site.register(InstituteProfile)
admin.site.register(TextWidget)
admin.site.register(ListWidget, ListWidgetAdmin)
admin.site.register(WidgetListItem)
