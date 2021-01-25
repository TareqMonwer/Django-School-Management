from django.contrib import admin

from .models import (
    InstituteProfile, TextWidget,
    ListWidget, WidgetListItem
)


admin.site.register(InstituteProfile)
admin.site.register(TextWidget)
admin.site.register(ListWidget)
admin.site.register(WidgetListItem)
