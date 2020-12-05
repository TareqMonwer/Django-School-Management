from django.urls import path, include
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
]
