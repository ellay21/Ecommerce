# payments/models.py

from django.db import models

class Payment(models.Model):
    # order_id will eventually reference an Order from the order-service
    order_id = models.IntegerField(unique=True, db_index=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Added amount for realism

    status = models.CharField(
        max_length=50,
        default='Pending',
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
            ('Refunded', 'Refunded'),
        ]
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True) # Mock transaction ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order_id} - Status: {self.status}"