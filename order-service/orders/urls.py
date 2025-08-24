
from django.urls import path
from .views import CartView, CartItemDeleteView, OrderView 

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartItemDeleteView.as_view(), name='cart-delete'),

    path('orders/', OrderView.as_view(), name='order-list-create'),
]