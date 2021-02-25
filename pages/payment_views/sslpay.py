from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from students.models import AdmissionStudent
from payments.models import SSLPayment


# Check if settings.DISALLOW_PAYMENT is False.
# otherwise, these variables can't be imported and will raise exception.
ssl_settings = {
    'store_id': settings.STORE_ID,
    'store_pass': settings.STORE_PASS,
    'issandbox': settings.SSL_ISSANDBOX
}


def store_admission_pay_record(post_body):
    try:
        SSLPayment.objects.create(
            transaction_id=post_body['tran_id'],
            payer=post_body['cus_name'],
            received_amount=post_body['total_amount'],
            pay_reason=SSLPayment.SSL_PAY_REASONS[0][0],
            payer_mobile=post_body['cus_phone'],
            payer_email=post_body['cus_email'],
            payer_city=post_body['cus_city'],
            payer_country=post_body['cus_country']
        )
        return True
    except:
        return False


def online_admission_sslpayment(request, pk):
    registrant = AdmissionStudent.objects.get(pk=pk)

    sslcommerz = SSLCOMMERZ(ssl_settings)

    post_body = {}
    post_body['total_amount'] = 10000.50
    post_body['currency'] = "BDT"
    post_body['tran_id'] = registrant.id
    post_body['success_url'] = "https://tareqmonwer.com"
    post_body['fail_url'] = "www.erpbud.com/blog/"
    post_body['cancel_url'] = "www.erpbud.com"
    post_body['emi_option'] = 0
    post_body['cus_name'] = registrant.name
    post_body['cus_email'] = registrant.email
    post_body['cus_phone'] = registrant.mobile_number
    post_body['cus_add1'] = registrant.current_address
    post_body['cus_city'] = registrant.city
    post_body['cus_country'] = "Bangladesh"
    post_body['product_profile'] = "general"
    post_body['product_name'] = 'Online Admission'
    post_body['product_category'] = 'Educational Service'
    post_body['shipping_method'] = 'NO'
    post_body['num_of_item'] = 1
    post_body['cus_postcode'] = '0000'

    response = sslcommerz.createSession(post_body)
    import pprint
    print(pprint.pprint(response))
    if response['status'] == 'SUCCESS':
        store_record = store_admission_pay_record(post_body)
        print(store_record)
        if store_record:
            return HttpResponseRedirect(response['GatewayPageURL'])
        else:
            return HttpResponse(
                "Failed to Store Payment Info, Contact Admins ASAP."
            )
    return HttpResponse(response)
