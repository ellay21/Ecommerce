from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user_id = models.IntegerField(db_index=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        default='Pending',
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by User {self.user_id}"


class CartItem(models.Model):
    user_id = models.IntegerField(db_index=True)

    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_id', 'product_id')

    def __str__(self):
        return f"CartItem: User {self.user_id}, Product {self.product_id}"


class UserProxyModel(User):
    class Meta:
        proxy = True
        app_label = "orders"
        verbose_name = "Proxy User"
        verbose_name_plural = "Proxy Users"

    def __str__(self):
        return self.username or f"User {self.id}"