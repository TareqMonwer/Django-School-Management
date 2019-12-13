from django.urls import path
from . import views


app_name = 'course'

urlpatterns = [
    path('add-course/', views.course, name='course'),
    path('course-list/', views.course_list, name='course-list'),
    path('add-section/', views.section, name='section'),
    path('section-list/', views.section_list, name='section-list'),
    path('add-course-attendance/', views.course_attendance, name='course_attendance'),
    path('course_attendance-list/', views.course_attendance_list, name='course_attendance-list'),
]
