from django.shortcuts import render
from orders.models import Order 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order  
from checkout.models import DeliveryInformation  
from django.shortcuts import render
from checkout.models import DeliveryInformation
from django.shortcuts import render
from orders.models import Order
from checkout.models import DeliveryInformation

def user_orders(request):
    user = request.user
    user_orders = Order.objects.filter(user=user).order_by('-id')

    delivery_infos = DeliveryInformation.objects.filter(user=user)

    delivery_info_map = {delivery_info.user_id: delivery_info for delivery_info in delivery_infos}

    for order in user_orders:
        delivery_info = delivery_info_map.get(order.user_id)
        order.delivery_info = delivery_info if delivery_info else None

        for order_item in order.orderitem_set.all():
            order_item.total_price = order_item.item.price * order_item.quantity

    return render(request, 'orders/user_orders.html', {'user_orders': user_orders})

@api_view(['GET'])
def orders_api_view(request):
    orders = Order.objects.filter(user=request.user)

    orders_data = [
        {
            'order_id': order.id,
            'total_price': order.total_price,
            'items': [
                {
                    'name': order_item.item.name,
                    'quantity': order_item.quantity,
                    'image_url': order_item.item.image.url if order_item.item.image else None,
                }
                for order_item in order.orderitem_set.all()
            ]
        }
        for order in orders
    ]

    return Response({'orders': orders_data})


@api_view(['GET'])
def user_orders_api_view(request, user_id):
    try:
        orders = Order.objects.filter(user_id=user_id)

        orders_data = [
            {
                'order_id': order.id,
                'total_price': order.total_price,
                'items': [
                    {
                        'name': order_item.item.name,
                        'quantity': order_item.quantity,
                        'image_url': request.build_absolute_uri(order_item.item.image.url) if order_item.item.image else None,
                    }
                    for order_item in order.orderitem_set.all()
                ]
            }
            for order in orders
        ]

        return Response({'orders': orders_data})

    except Order.DoesNotExist:
        return Response({'error': 'User orders not found'}, status=404)
