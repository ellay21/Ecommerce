from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer

class CartOrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    A unified ViewSet for managing the Shopping Cart and creating Orders.
    - list: Returns all items in the user's cart.
    - create: Adds a new item to the user's cart.
    - destroy: Removes an item from the user's cart.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'place_order':
            return OrderSerializer
        return CartItemSerializer

    def get_queryset(self):
        """This view should return a list of all cart items for the currently authenticated user."""
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the cart item with the current user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='place-order')
    def place_order(self, request):
        """
        Creates an order from the user's current cart items.
        """
        cart_items = self.get_queryset()
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create a JSON snapshot of the items
        order_items_snapshot = [{
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": str(item.product.price)
        } for item in cart_items]

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            order_items_snapshot=order_items_snapshot
        )

        # Clear the user's cart
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)