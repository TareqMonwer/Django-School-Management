import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django_school_management.students.models import AdmissionStudent
from django_school_management.students.tasks import send_admission_confirmation_email

def online_admission_stripepayment(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    registrant = get_object_or_404(AdmissionStudent, pk=pk)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('pages:stripe_payment_success', kwargs={'pk': pk})
        )
        cancel_url = request.build_absolute_uri(
            reverse('pages:stripe_payment_cancel', kwargs={'pk': pk})
        )
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            client_reference_id=str(pk),
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Online Admission Fee"},
                    "unit_amount": 2000,
                },
                "quantity": 1,
            }],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return redirect(checkout_session.url, code=303)

    # GET: show payment page
    context = {
        'registrant': registrant,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'pages/students/admission_stripe_payment.html', context)


def stripe_payment_success(request, pk):
    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    registrant.paid = True
    registrant.admitted = True
    registrant.save()
    send_admission_confirmation_email.delay(registrant.id)
    return render(request, 'pages/students/admission_payment_success.html', {
        'registrant': registrant
    })


def stripe_payment_cancel(request, pk):
    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    return render(request, 'pages/students/admission_payment_cancel.html', {
        'registrant': registrant
    })
