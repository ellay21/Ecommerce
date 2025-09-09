# payments/views.py
from rest_framework import viewsets, mixins, permissions
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    ViewSet for initiating and viewing payments.
    - create: Initiates a new payment for an order. The payment status will be 'Pending'.
    - list: Lists the user's past and pending payments.
    - retrieve: Retrieves the details of a specific payment.
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own payments."""
        return Payment.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        """
        Validates that the user owns the order they are trying to pay for.
        """
        order = serializer.validated_data['order']
        if order.user != self.request.user:
            self.permission_denied(
                self.request,
                message="You can only initiate payments for your own orders."
            )
        
        # In a real app, you would now get a transaction ID from a provider.
        # Here, we just save the payment in its initial 'Pending' state.
        serializer.save()