from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, AdmissionStudentViewSet

router = DefaultRouter()
router.register(r'applications', AdmissionStudentViewSet, basename='admission')
router.register(r'', StudentViewSet, basename='student')

app_name = 'students_api'

urlpatterns = [
    path('', include(router.urls)),
]
