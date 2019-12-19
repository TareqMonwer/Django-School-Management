from django.urls import path
from . import views


app_name = 'course'

urlpatterns = [
    path('add-course/', views.course, name='course'),
    path('course-list/', views.course_list, name='course-list'),
    path('add-section/', views.section, name='section'),
    path('section-list/', views.section_list, name='section-list'),
    path('attendance/', views.daily_attendance, name='daily-attendance'),
    path('add-course-attendance/', views.course_attendance, name='course-attendance'),
    path('course-attendance-list/', views.course_attendance_list, name='course-attendance-list'),
    path('add-course-assign-to-teacher/', views.course_assign_to_teacher, name='add-course-assign-to-teacher'),
    path('course-assign-to-teacher-list/', views.course_assign_to_teacher_list, name='course-assign-to-teacher-list'),
    path('add-course-assign-to-student/', views.course_assign_to_student, name='add-course-assign-to-student'),
    path('course-assign-to-student-list/', views.course_assign_to_student_list, name='course-assign-to-student-list'),

]
