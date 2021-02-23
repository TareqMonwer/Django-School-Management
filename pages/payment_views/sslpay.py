from students.models import AdmissionStudent
from sslcommerz_lib import SSLCOMMERZ


ssl_settings = {
    'store_id': 'yourstoreid',
    'store_pass': 'yourstorepassword',
    'issandbox': True
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
    pprint(response)

    if response['status'] == 'SUCCESS':
        return HttpResponseRedirect(response['GatewayPageURL'])
    return HttpResponse(response)

    