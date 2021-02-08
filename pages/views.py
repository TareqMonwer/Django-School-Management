import braintree

from config import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from academics.models import Department, Semester, AcademicSession, Subject
from result.models import SubjectGroup
from students.forms import StudentForm
from students.models import AdmissionStudent
from articles.models import Article
from students.tasks import send_admission_confirmation_email


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
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
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
            send_admission_confirmation_email(registrant.id)
            return redirect('pages:online_admission')


class UserGuideView(TemplateView):
    template_name = 'pages/user_guide.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        check_models = [Department, Semester, AcademicSession, Subject, SubjectGroup]
        models = []

        for model in check_models:
            model_count = model.objects.count() > 0 # returns bool
            if not model_count:
                model.classname = model.__name__
                models.append(model)
        context['models'] = models
        return self.render_to_response(context)

user_guide_view = UserGuideView.as_view()
