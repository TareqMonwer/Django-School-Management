from django.urls import path
from students.views import student_result_view

app_name = 'result'

urlpatterns = [
    path('<int:student_id>/<int:semester>/', student_result_view, name='show_result'),
]