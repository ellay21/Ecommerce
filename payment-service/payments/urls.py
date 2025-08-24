
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentProcessView, PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet) 
urlpatterns = [
    path('', include(router.urls)), 
    path('payments/process/', PaymentProcessView.as_view(), name='payment-process'), 
]