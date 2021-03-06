import django_tables2 as tables
from .models import (
    Newsletter
)


class NewsletterTable(tables.Table):
    class Meta:
        model  = Newsletter
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = (
            'created',
            'email'
        )