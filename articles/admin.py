from mptt.admin import MPTTModelAdmin
from mptt.models import TreeManyToManyField
from django.forms import CheckboxSelectMultiple
from django.contrib import admin

from .models import Article, Like, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['status',]

    formfield_overrides = {
        TreeManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', ]



# Registers
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # TODO: Display obj __str__ representation in list display.
    list_display = ['__str__', 'created']
