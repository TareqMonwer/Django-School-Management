from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, AdmissionStudentViewSet

router = DefaultRouter()
# Main resource at '' so URL is /api/v1/students/ not /api/v1/students/students/
router.register(r'', StudentViewSet, basename='student')
router.register(r'applications', AdmissionStudentViewSet, basename='admission')

app_name = 'students_api'

urlpatterns = [
    path('', include(router.urls)),
]
