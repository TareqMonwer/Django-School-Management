import django_tables2 as tables
from .models import (
    SSLAdmissionPaymentVerfication, 
    SSLPayment
)


class SSLPaymentTable(tables.Table):
    class Meta:
        model  = SSLPayment
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = (
            'created',
            'transaction_id',
            'payer',
            'received_amount',
            'pay_reason',
            'payer_mobile',
            'payer_city'
        )