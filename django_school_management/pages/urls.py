from django.urls import path
from django_school_management.pages.payment_views.sslpay import online_admission_sslpayment
from django_school_management.pages.payment_views.stripe_pay import (
     online_admission_stripepayment,
     stripe_payment_cancel,
     stripe_payment_success,
)
from . import views

app_name = 'pages'
urlpatterns = [
     path('', views.index, name='landing'),
     path('admission/', views.online_admission, name='online_admission'),
     path('admission/payment/<int:pk>/', views.online_admission_payment,
          name='online_admission_payment'
          ),
     path('admission/sslpayment/<int:pk>/', online_admission_sslpayment,
          name='online_admission_sslpayment'
     ),
     path('admission/stripepayment/<int:pk>/', online_admission_stripepayment,
          name='online_admission_stripepayment'
     ),
     path('admission/stripe-success/<int:pk>/', stripe_payment_success, name='stripe_payment_success'),
     path('admission/stripe-cancel/<int:pk>/', stripe_payment_cancel, name='stripe_payment_cancel'),
     path('admission/paynow/<int:pk>/', views.payment,
          name='payment'
          ),
     path('userguide/', views.user_guide_view,
          name='userguide'
          ),
]
