from django.urls import path

from . import views

app_name = 'result'

urlpatterns = [
    path('', views.result_view, name='result_home'),
    path('student/<int:student_pk>/', views.result_detail_view,
        name='result_detail_view'
    ),
]
