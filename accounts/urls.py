from django.urls import path, include
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.profile_complete, name='profile_complete'),
    path('auth/', include('django.contrib.auth.urls')),
    # register path is archived since we're using allauth'
    # path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('user-requests/', views.user_requests_list, name='user_requests'),
    path('permission-error/', views.permission_error, name='permission_error'),
    path('approval/<int:pk>/', views.user_approval, name='user_approval'),
    path('modify-and-approve/<int:pk>/',
        views.user_approval_with_modification,
        name='approval_with_modification'
    ),
]
