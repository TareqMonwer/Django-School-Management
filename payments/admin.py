from django.contrib import admin
from .models import SSLPayment, SSLAdmissionPaymentVerfication


@admin.register(SSLPayment)
class SSLPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'payer',
        'received_amount',
        'pay_reason',
        'payer_mobile',
        'payer_email'
    )


@admin.register(SSLAdmissionPaymentVerfication)
class SSLAdmissionPaymentVerficationAdmin(admin.ModelAdmin):
    list_display = (
        'payment',
        'status',
        'verified_by',
    )
