
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db import transaction # For atomic operations

from .models import CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer

# --- Existing Cart Views ---
class CartView(APIView):
    """Handles GET and POST for the shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user_id=request.user.id)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"product_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = CartItem.objects.get(user_id=request.user.id, product_id=product_id)
            item.quantity += int(quantity)
            item.save()
            serializer = CartItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CartItem.DoesNotExist:
            data = {'product_id': product_id, 'quantity': quantity}
            serializer = CartItemSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteView(APIView):
    """Handles DELETE /cart/{item_id}/"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, user_id=request.user.id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- New Order Views ---
class OrderView(APIView):
    """Handles POST to place a new order and GET for order history."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all orders for the authenticated user."""
        orders = Order.objects.filter(user_id=request.user.id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Place a new order from the user's current cart."""
        user_id = request.user.id
        cart_items = CartItem.objects.filter(user_id=user_id)

        if not cart_items.exists():
            return Response({"detail": "Your cart is empty. Cannot place an order."},
                            status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        for item in cart_items:
            total_amount += item.quantity * 10 # Dummy price for each product

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user_id=user_id,
                    total=total_amount,
                    status='Pending' 
                )

                cart_items.delete()

                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Error placing order: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
