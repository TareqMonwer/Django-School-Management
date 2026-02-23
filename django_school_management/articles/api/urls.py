from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
# Main resource at '' so URL is /api/v1/articles/ not /api/v1/articles/articles/
router.register(r'', ArticleViewSet, basename='article')

app_name = 'articles_api'

urlpatterns = [
    path('', include(router.urls)),
]
