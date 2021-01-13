from django.urls import path, include
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.profile_complete, name='profile_complete'),
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('user-requests/', views.user_requests_list, name='user_requests'),
    path('permission-error/', views.permission_error, name='permission_error'),
    path('approval/<int:pk>/', views.user_approval, name='user_approval'),
]
