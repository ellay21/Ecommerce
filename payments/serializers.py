# payments/serializers.py
from rest_framework import serializers
from .models import Payment
from orders.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    # This field allows us to specify which order we are paying for when we POST
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'order', 'status', 'created_at', 'updated_at']
        # The following fields should not be settable by the user directly
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'order']
        depth = 1 # This will show nested order details when we GET a payment