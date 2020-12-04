from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='landing'),
    path('admission/', views.online_admission, name='online_admission'),
    path('admission/payment/<int:pk>/', views.online_admission_payment,
         name='online_admission_payment'),
    path('admission/paynow/<int:pk>/', views.payment,
         name='payment'),
]
