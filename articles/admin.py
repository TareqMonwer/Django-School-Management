from mptt.admin import MPTTModelAdmin
from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

from .models import Article, Like, Category



# # Resources for import export.
# class ArticleResource(resources.ModelResource):
#     class Meta:
#         model = Article


# Admin classes.
# class ArticleAdmin(ImportExportModelAdmin):
#     list_display = ['title', 'author', 'status']
#     resource_class = ArticleResource

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['status',]


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', ]



# Registers
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # TODO: Display obj __str__ representation in list display.
    list_display = ['__str__', 'created']
