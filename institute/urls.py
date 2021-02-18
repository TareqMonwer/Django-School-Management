from django.urls import path
from . import views


app_name = 'institute'
urlpatterns = [
    path('dashboard/settings/<int:institute_pk>/', 
        views.InstituteProfileConfigDashboard.as_view(), 
        name='institute_config'
    ),
    path('dashboard/settings/detail/<int:institute_pk>/',
        views.InstituteProfileDetailDashboard.as_view(),
        name='institute_detail'
    ),
]