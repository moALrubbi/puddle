from django.shortcuts import render
from orders.models import Order  # Import the Order model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order  # Import your Order model
from checkout.models import DeliveryInformation  # Import the DeliveryInformation model from checkout
from django.shortcuts import render
from orders.models import Order
from checkout.models import DeliveryInformation
from django.shortcuts import render
from orders.models import Order
from checkout.models import DeliveryInformation

def user_orders(request):
    user = request.user
    user_orders = Order.objects.filter(user=user).order_by('-id')

    # Fetch delivery information associated with user's orders
    delivery_infos = DeliveryInformation.objects.filter(user=user)

    # Create a dictionary mapping order IDs to delivery information
    delivery_info_map = {delivery_info.user_id: delivery_info for delivery_info in delivery_infos}

    for order in user_orders:
        delivery_info = delivery_info_map.get(order.user_id)
        order.delivery_info = delivery_info if delivery_info else None

        # Calculate the total price for each item in each order
        for order_item in order.orderitem_set.all():
            order_item.total_price = order_item.item.price * order_item.quantity

    return render(request, 'orders/user_orders.html', {'user_orders': user_orders})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order

@api_view(['GET'])
def orders_api_view(request):
    # Fetch orders for the current user from the database
    orders = Order.objects.filter(user=request.user)

    # Serialize orders data (convert to JSON or desired format)
    orders_data = [
        {
            'order_id': order.id,
            'total_price': order.total_price,
            'items': [
                {
                    'name': order_item.item.name,
                    'quantity': order_item.quantity,
                    'image_url': order_item.item.image.url if order_item.item.image else None,
                    # Include other item details as needed (e.g., price, description)
                }
                for order_item in order.orderitem_set.all()
            ]
        }
        for order in orders
    ]

    # Return orders data as JSON response
    return Response({'orders': orders_data})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order

@api_view(['GET'])
def user_orders_api_view(request, user_id):
    try:
        # Fetch orders for the specified user ID from the database
        orders = Order.objects.filter(user_id=user_id)

        # Serialize orders data (convert to JSON or desired format)
        orders_data = [
            {
                'order_id': order.id,
                'total_price': order.total_price,
                'items': [
                    {
                        'name': order_item.item.name,
                        'quantity': order_item.quantity,
                        'image_url': order_item.item.image.url if order_item.item.image else None,
                        # Include other item details as needed (e.g., price, description)
                    }
                    for order_item in order.orderitem_set.all()
                ]
            }
            for order in orders
        ]

        # Return orders data as JSON response
        return Response({'orders': orders_data})

    except Order.DoesNotExist:
        return Response({'error': 'User orders not found'}, status=404)
