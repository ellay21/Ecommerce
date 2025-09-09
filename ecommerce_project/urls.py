from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
