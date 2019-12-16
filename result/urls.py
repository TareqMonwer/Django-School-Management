from django.urls import path

from . import views
from students.views import student_result_view

app_name = 'result'

urlpatterns = [
    path('<int:student_id>/<int:semester>/', student_result_view, name='show_result'),
    path('details/<int:student_id>/<int:semester>/',
         views.show_result_by_semester, name='result_by_semester'),
    path('upload-subjects-csv/', views.upload_subjects_csv, name='import_subject_csv'),
]
