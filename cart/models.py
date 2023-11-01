from django.db import models
from django.contrib.auth.models import User
from item.models import Item  # Import the Item model from the 'item' app

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='carts')  # Establish a many-to-many relationship with the Item model

    # Additional fields or methods related to the Cart model
