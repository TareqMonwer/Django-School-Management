from import_export import resources
from mptt.admin import MPTTModelAdmin
from mptt.models import TreeManyToManyField
from django.forms import CheckboxSelectMultiple
from django.contrib import admin

from .models import Article, Like, Category, Newsletter


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created',
        'force_highlighted', 'status'
    ]
    list_editable = ['status', 'force_highlighted']
    list_filter = ['status', 'force_highlighted',
        'author', 'created'
    ]
    list_per_page = 25

    formfield_overrides = {
        TreeManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]


# Registers
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Newsletter)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # TODO: Display obj __str__ representation in list display.
    list_display = ['__str__', 'created']
