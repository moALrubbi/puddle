#item/models.py

from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    stocks = models.PositiveIntegerField(default=1)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='user_items', on_delete=models.CASCADE)  # Change the related_name to 'user_items'
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_cart')  # Change the related_name to 'user_cart'
    total_price = models.FloatField(default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)  # Change the related_name to 'cart_items'
    item = models.ForeignKey(Item, related_name='item_cart_items', on_delete=models.CASCADE)  # Change the related_name to 'item_cart_items'
    quantity = models.IntegerField(default=1)

