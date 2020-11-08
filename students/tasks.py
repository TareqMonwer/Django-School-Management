from celery.decorators import task
from celery.utils.log import get_logger

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

from .models import AdmissionStudent

logger = get_logger(__name__)


@task(name='send_admission_confirmation_email')
def send_admission_confirmation_email(student_id):
    student = AdmissionStudent.objects.get(id=student_id)
    name = student.name
    choosen_dept = student.choosen_department
    send_mail(
        f'SMS-LIO: Admission confirmed for student {name}',
        f'Choosen Dept: {choosen_dept}',
        EMAIL_HOST_USER,
        [student.email, ], 
        fail_silently=False
    )