from django.contrib import admin
from .models import DeliveryInformation, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_items', 'get_quantity', 'total_price')

    def get_items(self, obj):
        return ', '.join([order_item.item.name for order_item in obj.orderitem_set.all()])
    get_items.short_description = 'Items'  # Display name for the items field

    def get_quantity(self, obj):
        return sum([order_item.quantity for order_item in obj.orderitem_set.all()])
    get_quantity.short_description = 'Total Quantity'  # Display name for the quantity field

    def total_price(self, obj):
        total = sum([order_item.item.price * order_item.quantity for order_item in obj.orderitem_set.all()])
        return f'${total:.2f}'  # Display total price in currency format
    total_price.short_description = 'Total Price'  # Display name for the total price field

class DeliveryInformationAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'first_name', 'last_name', 'street_name', 'city', 'postal_code', 'phone_number')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number')
    # Add any other configurations as needed
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryInformation, DeliveryInformationAdmin)