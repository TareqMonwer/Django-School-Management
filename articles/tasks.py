from celery.decorators import task
from celery.utils.log import get_logger

from django.core.mail import send_mail
from django.core import serializers
from config.settings import EMAIL_HOST_USER
from .models import Article


logger = get_logger(__name__)


@task(name='send_latest_article')
def send_latest_article(mail_list, article_id):
    article = Article.objects.get(id=article_id)
    deserialized_mail_list = serializers.deserialize("json", mail_list, ignorenonexistent=True)
    send_mail(
        f'Read Latest Article: {article.title}',
        f'{article.title}',
        EMAIL_HOST_USER,
        [subscriber.object.email for subscriber in deserialized_mail_list], 
        fail_silently=False
    )