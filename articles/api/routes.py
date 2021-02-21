from rest_framework import routers
from django.urls import path, include
from .views import ArticleViewSet


router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]