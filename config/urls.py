from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account.views import dashboard


admin.site.site_header = "SMS-LIO Admin"
admin.site.site_title = "SMS-LIO Admin Portal"
admin.site.index_title = "Welcome to SMS-LIO Portal"

urlpatterns = [
    path('__debug__', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', dashboard, name='index_view'),
    path('account/', include('account.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('result/', include('result.urls')),
    path('misc/', include('admin_tools.urls')),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/password_reset.html'
        ),
        name="password_reset",
    ),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password/password_reset_confirm.html'
        ),
        name="password_reset_confirm",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
