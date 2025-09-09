# payments/webhook_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Payment, Order

class PaymentWebhookView(APIView):
    """
    A mock webhook endpoint for a payment provider to send updates.
    This endpoint is public and is where the payment status is confirmed.
    """
    permission_classes = [AllowAny] # Webhooks do not use user authentication

    def post(self, request, *args, **kwargs):
        payload = request.data
        payment_id = payload.get('payment_id')
        event_type = payload.get('event_type') # e.g., 'payment.succeeded'

        if not payment_id or not event_type:
            return Response(
                {"error": "Missing 'payment_id' or 'event_type' in payload."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # `select_related` is a performance optimization
            payment = Payment.objects.select_related('order').get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        if event_type == 'payment.succeeded':
            payment.status = 'Success'
            payment.order.status = 'Completed'
        elif event_type == 'payment.failed':
            payment.status = 'Failed'
            payment.order.status = 'Cancelled'
        else:
            # We can just ignore events we don't care about
            return Response(status=status.HTTP_200_OK)

        payment.save()
        payment.order.save() # Save the related order as well

        return Response({"status": "webhook received"}, status=status.HTTP_200_OK)