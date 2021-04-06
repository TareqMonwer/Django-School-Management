from django.urls import path
from notices.views import dashboard_views as views

app_name = 'notices_dashboard'
urlpatterns = [
    path('publish/', views.publish_notice_documents, name='publish_notice_documents'),
    path('publish/<int:notice_pk>/', views.publish_notice_documents, name='publish_notice_documents'),
]
