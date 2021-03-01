from celery.decorators import task
from celery.utils.log import get_logger

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


logger = get_logger(__name__)


@task(name='send_latest_article')
def send_latest_article(mail_list, article):
    send_mail(
        f'Read Latest Article: {article.title}',
        f'{article.title}',
        EMAIL_HOST_USER,
        [subscriber.email for subscriber in mail_list], 
        fail_silently=False
    )