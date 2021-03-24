from django.urls import path
from notices.views import site_views as views


app_name = 'notices'
urlpatterns = [
    path('', views.NoticesPageView.as_view(), name='notices'),
]