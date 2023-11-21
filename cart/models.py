#cart/models.py
from django.db import models
from django.contrib.auth.models import User
from item.models import Item  # Import the Item model from the 'item' app

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='carts')  # Establish a many-to-many relationship with the Item model
    total_price = models.FloatField(default=0)  # Field to save the total price

    # Additional fields or methods related to the Cart model

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item.name


def update_stocks(item, quantity):
    """
    Update the stocks of an item based on the given quantity.
    """
    if quantity <= item.stocks:
        item.stocks = max(item.stocks - quantity, 0)
        item.save()
    else:
        # Handle insufficient stock, e.g., notify the user or adjust the quantity
        # You might raise an exception, log a warning, or take other appropriate actions
        print(f"Insufficient stock for item {item.name}")
