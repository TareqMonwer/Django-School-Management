from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create router and register viewsets here
router = DefaultRouter()
# router.register(r'departments', DepartmentViewSet, basename='department')
# router.register(r'batches', BatchViewSet, basename='batch')
# router.register(r'subjects', SubjectViewSet, basename='subject')

app_name = 'academics_api'

urlpatterns = [
    path('', include(router.urls)),
]
