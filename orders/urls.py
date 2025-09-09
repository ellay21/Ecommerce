from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartOrderViewSet

router = DefaultRouter()
router.register(r'cart', CartOrderViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]