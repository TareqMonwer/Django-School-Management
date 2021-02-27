from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('sslpays/', views.dashboard_ssl_payments_list, 
        name='dashboard_ssl_payments_list'
    ),
]