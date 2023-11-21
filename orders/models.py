# orders/models.py

from django.db import models
from checkout.models import Order  # Import Order model

class UserOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='user_order')
    # Add other fields if necessary

    def __str__(self):
        return f"User Order #{self.order.pk}"
