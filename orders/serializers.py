from rest_framework import serializers
from .models import CartItem, Order
from products.serializers import ProductSerializer # We'll nest product info
from products.models import Product
class CartItemSerializer(serializers.ModelSerializer):
    # Nest the full product details for easier display on the frontend
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'created_at']
        read_only_fields = ['id', 'created_at', 'product']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'order_items_snapshot', 'total_price', 'created_at')