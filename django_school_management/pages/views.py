from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django_school_management.academics.models import Department
from django_school_management.students.forms import StudentForm
from django_school_management.students.models import AdmissionStudent
from django_school_management.mixins.institute import get_active_institute
from django_school_management.articles.models import Article
from django_school_management.students.tasks import send_admission_confirmation_email


def index(request):
    blog_count = Article.objects.count()
    departments = Department.objects.all()
    if blog_count >= 3:
        recent_blogs = Article.objects.order_by('-created')[:3]
    else:
        recent_blogs = Article.objects.order_by('-created')[:blog_count]
    ctx = {
        'recent_blogs': recent_blogs,
        'departments': departments,
    }
    return render(request, 'website/index.html', ctx)


def online_admission(request):
    institute = get_active_institute()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, institute=institute)
        if form.is_valid():
            data = form.save()
            if settings.USE_STRIPE:
                return redirect('pages:online_admission_stripepayment', pk=data.pk)
            return redirect('pages:online_admission_sslpayment', pk=data.pk)
    else:
        form = StudentForm(institute=institute)
    # For template JS: show JSC section only when applying for class 9-10 (BD school/madrasah)
    show_jsc_conditional = (
        institute and getattr(institute, 'country', None) and
        str(getattr(institute.country, 'code', institute.country)) == 'BD' and
        getattr(institute, 'is_school_or_madrasah', False)
    )
    # For template JS: show admit_to_semester only when HSC Science (BD polytechnic)
    show_admit_semester_conditional = (
        institute and getattr(institute, 'country', None) and
        str(getattr(institute.country, 'code', institute.country)) == 'BD' and
        getattr(institute, 'is_polytechnic', False)
    )
    return render(request, 'pages/students/admission.html', {
        'form': form,
        'institute': institute,
        'show_jsc_conditional': show_jsc_conditional,
        'show_admit_semester_conditional': show_admit_semester_conditional,
    })


def online_admission_payment(request, pk):
    """
    Braintree payment flow (currently deferred -- PayPal not available in region).
    Generates nonce and renders payment form.
    """
    import braintree

    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    braintree_env = braintree.Environment.Sandbox

    try:
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
    except Exception:
        messages.error(request, "Payment gateway is not configured properly.")
        return redirect('pages:online_admission')

    try:
        braintree_client_token = braintree.ClientToken.generate({})
    except Exception:
        messages.error(request, "Could not initialize payment. Please try again.")
        return redirect('pages:online_admission')

    context = {
        'braintree_client_token': braintree_client_token,
        'registrant': registrant,
    }
    return render(request, 'pages/students/admission_payment.html', context)


def payment(request, pk):
    """
    Handles the Braintree payment from student registrant.
    """
    import braintree

    registrant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == 'POST':
        nonce_from_the_client = request.POST.get('paymentMethodNonce')
        customer_kwargs = {
            'first_name': registrant.name,
            'email': registrant.email,
        }
        try:
            customer_create = braintree.Customer.create(customer_kwargs)
            customer_id = customer_create.customer.id
            result = braintree.Transaction.sale({
                "amount": 100,
                "payment_method_nonce": nonce_from_the_client,
                "options": {"submit_for_settlement": True},
            })
        except Exception:
            messages.error(request, "Payment processing failed. Please try again.")
            return redirect('pages:online_admission_payment', pk=pk)

        if result.is_success:
            registrant.paid = True
            registrant.save()
            try:
                send_admission_confirmation_email(registrant.id)
            except Exception:
                pass
            messages.success(request, "Payment successful! Your application has been received.")
            return redirect('pages:online_admission')
        else:
            messages.error(request, "Payment was declined. Please try again.")
            return redirect('pages:online_admission_payment', pk=pk)

    return redirect('pages:online_admission_payment', pk=pk)
