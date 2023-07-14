import django_filters
from .models import SSLPayment

class SSLPaymentFilter(django_filters.FilterSet):
    class Meta:
        model = SSLPayment
        fields = [
            'transaction_id',
            'pay_reason',
            'payer_mobile',
            'payer',
        ]