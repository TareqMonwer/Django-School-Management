from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

from .models import Article, Like



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
    list_editable = ['status', ]



# Registers
admin.site.register(Article, ArticleAdmin)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # TODO: Display obj __str__ representation in list display.
    list_display = ['__str__', 'created']
