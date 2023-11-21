#cart/admin.py
from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items')  # Fields to display in the admin list

    def get_items(self, obj):
        return "\n".join([str(item) for item in obj.items.all()])
    get_items.short_description = 'Items'

