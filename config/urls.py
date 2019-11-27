"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import index_view
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "SMS-LIO Admin"
admin.site.site_title = "SMS-LIO Admin Portal"
admin.site.index_title = "Welcome to SMS-LIO Portal"

urlpatterns = [
    path('__debug__', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', index_view, name='index_view'),
    path('account/', include('account.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('result/', include('result.urls')),
    path('misc/', include('admin_tools.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
