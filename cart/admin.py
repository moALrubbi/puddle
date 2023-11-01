from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items')  # Example fields to display in the admin list
    # Additional customizations or methods for the Cart admin view

    def get_items(self, obj):
        return "\n".join([str(item) for item in obj.items.all()])
    get_items.short_description = 'Items'
