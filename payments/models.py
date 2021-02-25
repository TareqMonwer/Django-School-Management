from model_utils.models import TimeStampedModel
from django.conf import settings
from django.db import models


class SSLPayment(TimeStampedModel):
    """ Table to store payment records coming from
    admission form.
    Recommended way to create this class's instance is
    only after a successfull admission payment.
    """

    # NOTE: DO NOT CHANGE THE ORDER OF TUPLE ITEMS.
    SSL_PAY_REASONS = (
        ('admission', 'Online Admission'),
        ('midfee', 'Midterm Exam Fee'),
        ('finalfee', 'Final Exam Fee'),
    )
    transaction_id = models.PositiveIntegerField()
    payer = models.CharField("Name of the registrant",
        max_length=150
    )
    received_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    pay_reason = models.CharField(
        max_length=10,
        choices=SSL_PAY_REASONS
    )
    payer_mobile = models.CharField(max_length=15)
    payer_email = models.EmailField()
    # By 2021, longest city name has 85 chars.
    payer_city = models.CharField(max_length=85)
    payer_country = models.CharField(max_length=55)

    class Meta:
        verbose_name_plural = 'SSL Payment'
        ordering = ['-created', 'received_amount']
    
    def __str__(self):
        return f'TransID #{self.transaction_id}'


class SSLAdmissionPaymentVerfication(TimeStampedModel):
    VERIFICATION_STATUS = (
        (0, 'Rejected'),
        (1, 'Verfied')
    )
    payment = models.ForeignKey(
        SSLPayment,
        on_delete=models.CASCADE,
        related_name='verfied_payments'
    )
    status = models.PositiveSmallIntegerField(
        choices=VERIFICATION_STATUS,
        default=0
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='admission_pay_verifications',
    )

    class Meta:
        verbose_name_plural = 'SSL Admission Payment Verfication'
        ordering = ['-created', ]
    
    def __str__(self):
        return f'{self.payment} {self.status} by {self.verified_by}'
