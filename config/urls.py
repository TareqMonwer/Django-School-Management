from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from institute.models import InstituteProfile
from accounts.views import dashboard

try:
    institute = InstituteProfile.objects.get(active=True)
    admin.site.site_header = institute.site_header
    admin.site.site_title = institute.site_title
    admin.site.index_title = institute.index_title
except:
    admin.site.site_header = 'Django Administration'
    admin.site.site_title = 'Django Site Admin'
    admin.site.index_title = 'Django Administration'

DJANGO_ADMIN_URL = settings.DJANGO_ADMIN_URL + '/'

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(DJANGO_ADMIN_URL, admin.site.urls),
    path('', include('pages.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('dashboard/', dashboard, name='index_view'),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('articles.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('notices/', include('notices.site_urls')),
    path('notices/dashboard/', include('notices.dashboard_urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('result/', include('result.urls')),
    path('institute/', include('institute.urls')),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/password_reset.html'
        ),
        name="password_reset",
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password/password-reset-complete.html'
        ),
        name='password_reset_complete'
    ),
    path('dashboard/payments/', include('payments.urls')),
    # API URLS
    path('api/', include('articles.api.routes')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
