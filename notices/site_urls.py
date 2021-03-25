from django.urls import path
from notices.views import site_views as views


app_name = 'notices'
urlpatterns = [
    path('', views.NoticesPageView.as_view(), name='notices'),
    path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
]
