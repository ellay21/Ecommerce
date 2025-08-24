# payments/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import uuid # For mock transaction IDs

from .models import Payment
from .serializers import PaymentSerializer
from .tasks import async_process_payment # Import our Celery task

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing payment details.
    (Only Read operations, as creation is handled by PaymentProcessView)
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentProcessView(APIView):
    """
    Handles POST requests to initiate a new payment.
    """

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        if not order_id or not amount:
            return Response({"detail": "Both 'order_id' and 'amount' are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if Payment.objects.filter(order_id=order_id).exists():
            return Response({"detail": f"Payment for order {order_id} already initiated."},
                            status=status.HTTP_409_CONFLICT) # 409 Conflict

        payment = Payment.objects.create(
            order_id=order_id,
            amount=amount,
            status='Pending',
        )

        async_process_payment.delay(payment.id) 

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 