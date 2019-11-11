from django.urls import path
from . import views


app_name = 'teachers'

urlpatterns = [
    path('', views.teachers_view, name='all_teacher'),
    path('add/', views.add_teacher_view, name='add_teacher'),
    path('<int:pk>/details/', views.teacher_detail_view, name='teacher_details'),
    path('<int:pk>/update/', views.teacher_update_view.as_view(), name='update_teacher'),
]