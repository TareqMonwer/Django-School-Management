import braintree

from config import settings
from django.shortcuts import render, redirect
from students.forms import StudentForm
from students.models import AdmissionStudent

from students.tasks import send_admission_confirmation_email


def index(request):
    return render(request, 'landing/index.html')


def online_admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            print(data)
            return redirect('pages:online_admission_payment', pk=data.pk)
    else:
        form = StudentForm()
    return render(request, 'pages/students/admission.html', {'form': form})


def online_admission_payment(request, pk):
    """ 
    Generates nonce and renders payment form
    """
    registrant = AdmissionStudent.objects.get(pk=pk)
    braintree_env = braintree.Environment.Sandbox
    # Configure braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
    try:
        braintree_client_token = braintree.ClientToken.generate(
            {"registrant": registrant.id})
    except:
        braintree_client_token = braintree.ClientToken.generate({})
    context = {
        'braintree_client_token': braintree_client_token, 
        'registrant': registrant,
    }
    return render(request, 'pages/students/admission_payment.html', context)


def payment(request, pk):
    """ 
    Handles the payment from student registrant
    """
    registrant = AdmissionStudent.objects.get(pk=pk)
    if request.method == 'POST':
        nonce_from_the_client = request.POST.get('paymentMethodNonce')
        customer_kwargs = {
            'first_name': registrant.name,
            'email': registrant.email
        }
        customer_create = braintree.Customer.create(customer_kwargs)
        customer_id = customer_create.customer.id
        result = braintree.Transaction.sale({
            "amount": 100, 
            "payment_method_nonce": nonce_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })
        # mark registrant payment as done if payment is done.
        if result.is_success:
            registrant.paid = True
            registrant.admitted = True
            registrant.save()
            print(registrant.email)
            send_admission_confirmation_email(registrant.id)
            return redirect('pages:online_admission')
