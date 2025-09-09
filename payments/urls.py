# payments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
from .webhook_views import PaymentWebhookView # <-- Import the new view

router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    #webhook URL
    path('payments/webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]