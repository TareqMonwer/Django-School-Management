from django.urls import path
from . import views


app_name = 'institute'
urlpatterns = [
    # Onboarding wizard
    path('onboarding/',
        views.onboarding_step1,
        name='onboarding_step1'
    ),
    path('onboarding/academics/',
        views.onboarding_step2,
        name='onboarding_step2'
    ),
    path('onboarding/review/',
        views.onboarding_step3,
        name='onboarding_step3'
    ),

    # Settings pages
    path('dashboard/settings/institute-profiles/',
        views.InstituteProfileConfigListView.as_view(),
        name='institute_profile_list'
    ),
    path('dashboard/settings/setup-school/',
        views.InstituteProfileSetupDashboard.as_view(),
        name='setup_school'
    ),
    path('dashboard/settings/<int:institute_pk>/',
        views.InstituteProfileConfigDashboard.as_view(),
        name='institute_config'
    ),
    path('dashboard/settings/detail/<int:institute_pk>/',
        views.InstituteProfileDetailDashboard.as_view(),
        name='institute_detail'
    ),
    path('dashboard/settings/<int:institute_pk>/set-default/',
        views.SetActiveInstituteProfile.as_view(),
        name='set_default_institute'
    ),
]