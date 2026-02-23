from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create router and register viewsets here
router = DefaultRouter()
# router.register(r'teachers', TeacherViewSet, basename='teacher')

app_name = 'teachers_api'

urlpatterns = [
    path('', include(router.urls)),
]
