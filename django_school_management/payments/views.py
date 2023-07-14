from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import ListView
from .models import SSLPayment
from .tables import SSLPaymentTable
from .filters import SSLPaymentFilter


class DashboardSSLPaymentsList(SingleTableMixin, FilterView):
    model = SSLPayment
    table_class = SSLPaymentTable
    template_name = 'payments/dashboard/sslpayments.html'
    filterset_class = SSLPaymentFilter

dashboard_ssl_payments_list = DashboardSSLPaymentsList.as_view()