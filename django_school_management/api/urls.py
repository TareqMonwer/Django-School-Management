"""
Central API URL config. All routes are under /api/ (see config/urls.py).

Convention: path('v1/<resource>/', include('<app>.api.urls')) defines the resource
path. In each app's api/urls.py, register the main viewset with prefix r'' so
the final URL is /api/v1/<resource>/ (not /api/v1/<resource>/<resource>/).
Sub-resources use a non-empty prefix, e.g. router.register(r'applications', ...).
"""
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Django School Management API",
        default_version='v1',
        description="Comprehensive API for school management system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # API Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API Endpoints
    path('v1/students/', include('django_school_management.students.api.urls')),
    path('v1/academics/', include('django_school_management.academics.api.urls')),
    path('v1/teachers/', include('django_school_management.teachers.api.urls')),
    path('v1/payments/', include('django_school_management.payments.api.urls')),
    path('v1/articles/', include('django_school_management.articles.api.urls')),
]
