import logging

from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django_school_management.students.models import AdmissionStudent
from django_school_management.payments.models import SSLPayment

logger = logging.getLogger(__name__)

ssl_settings = {
    'store_id': settings.STORE_ID,
    'store_pass': settings.STORE_PASS,
    'issandbox': settings.SSL_ISSANDBOX,
}


def _store_admission_pay_record(post_body):
    try:
        SSLPayment.objects.create(
            transaction_id=post_body['tran_id'],
            payer=post_body['cus_name'],
            received_amount=post_body['total_amount'],
            pay_reason=SSLPayment.SSL_PAY_REASONS[0][0],
            payer_mobile=post_body['cus_phone'],
            payer_email=post_body['cus_email'],
            payer_city=post_body['cus_city'],
            payer_country=post_body['cus_country'],
        )
        return True
    except Exception:
        logger.exception("Failed to store SSL payment record")
        return False


def online_admission_sslpayment(request, pk):
    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    sslcommerz = SSLCOMMERZ(ssl_settings)

    base_url = request.build_absolute_uri('/')[:-1]
    post_body = {
        'total_amount': 10000.50,
        'currency': 'BDT',
        'tran_id': str(registrant.id),
        'success_url': base_url + reverse('pages:ssl_payment_success', args=[pk]),
        'fail_url': base_url + reverse('pages:ssl_payment_fail', args=[pk]),
        'cancel_url': base_url + reverse('pages:ssl_payment_cancel', args=[pk]),
        'emi_option': 0,
        'cus_name': registrant.name,
        'cus_email': registrant.email,
        'cus_phone': registrant.mobile_number,
        'cus_add1': registrant.current_address,
        'cus_city': str(registrant.city) if registrant.city else '',
        'cus_country': str(registrant.city.country) if registrant.city else '',
        'product_profile': 'general',
        'product_name': 'Online Admission',
        'product_category': 'Educational Service',
        'shipping_method': 'NO',
        'num_of_item': 1,
        'cus_postcode': '0000',
    }

    response = sslcommerz.createSession(post_body)
    if response.get('status') == 'SUCCESS':
        if _store_admission_pay_record(post_body):
            return HttpResponseRedirect(response['GatewayPageURL'])
        else:
            messages.error(request, "Failed to store payment info. Please contact support.")
            return redirect('pages:online_admission')

    logger.error("SSLCommerz session creation failed: %s", response)
    messages.error(request, "Could not initiate payment. Please try again later.")
    return redirect('pages:online_admission')


@csrf_exempt
def ssl_payment_success(request, pk):
    """SSLCommerz redirects here after successful payment."""
    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    registrant.paid = True
    registrant.save()
    messages.success(request, "Payment successful! Your application has been received.")
    return redirect('pages:online_admission')


@csrf_exempt
def ssl_payment_fail(request, pk):
    """SSLCommerz redirects here after a failed payment."""
    messages.error(request, "Payment failed. Please try again or contact support.")
    return redirect('pages:online_admission_sslpayment', pk=pk)


@csrf_exempt
def ssl_payment_cancel(request, pk):
    """SSLCommerz redirects here when the user cancels."""
    messages.warning(request, "Payment was cancelled.")
    return redirect('pages:online_admission')
