from sslcommerz_lib import SSLCOMMERZ
from django.http import HttpResponseRedirect, HttpResponse
from students.models import AdmissionStudent
from django.conf import settings

# Check if settings.DISALLOW_PAYMENT is False.
# otherwise, these variables can't be imported and will raise exception.
ssl_settings = {
    'store_id': settings.STORE_ID,
    'store_pass': settings.STORE_PASS,
    'issandbox': settings.SSL_ISSANDBOX
}

def online_admission_sslpayment(request, pk):
    registrant = AdmissionStudent.objects.get(pk=pk)

    sslcommerz = SSLCOMMERZ(ssl_settings)

    post_body = {}
    post_body['total_amount'] = 100.26
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = "https://tareqmonwer.com"
    post_body['fail_url'] = "www.erpbud.com/blog/"
    post_body['cancel_url'] = "www.erpbud.com"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    response = sslcommerz.createSession(post_body)
    if response['status'] == 'SUCCESS':
        return HttpResponseRedirect(response['GatewayPageURL'])
    return HttpResponse(response)

    