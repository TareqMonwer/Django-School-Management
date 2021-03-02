from pathlib import Path
from celery.decorators import task
from celery.utils.log import get_logger

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import serializers
from config.settings import EMAIL_HOST_USER
from .models import Article


logger = get_logger(__name__)


@task(name='send_latest_article')
def send_latest_article(mail_list, article_id):
    article = Article.objects.get(id=article_id)
    deserialized_mail_list = serializers.deserialize("json", mail_list, ignorenonexistent=True)

    html_template = Path('articles/newsletter-template.html')
    html_message = render_to_string(html_template, { 'article': article, })
    
    message = EmailMessage(
        'DPI JUST PUBLISHED NEW ARTICLE! READ IT', 
        html_message, 
        EMAIL_HOST_USER, 
        [subscriber.object.email for subscriber in deserialized_mail_list]
    )
    message.content_subtype = 'html'
    message.send()