from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create router and register viewsets here
router = DefaultRouter()
# router.register(r'payments', PaymentViewSet, basename='payment')

app_name = 'payments_api'

urlpatterns = [
    path('', include(router.urls)),
]
