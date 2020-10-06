from django.urls import path
from . import views


app_name = 'pages'
urlpatterns = [
    path('admission/', views.online_admission, name='online_admission'),
]