from django.urls import path

from . import views

app_name = 'result'

urlpatterns = [
    path('', views.result_view, name='result'),
]
