from django.urls import path
from pages.payment_views.sslpay import online_admission_sslpayment
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
     path('admission/paynow/<int:pk>/', views.payment,
          name='payment'
     ),
     path('userguide/', views.user_guide_view,
          name='userguide'
     ),
]
