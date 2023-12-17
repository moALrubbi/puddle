# checkout/views.py
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, update_stocks
from item.models import Item
from .models import Order, OrderItem
from .forms import CheckoutForm
from orders.models import UserOrder
from django.db.models import F 
@login_required
def checkout(request):
    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST)

        if checkout_form.is_valid():
            first_name = checkout_form.cleaned_data['first_name']
            last_name = checkout_form.cleaned_data['last_name']
            street_name = checkout_form.cleaned_data['street_name']
            building_number = checkout_form.cleaned_data['building_number']
            postal_code = checkout_form.cleaned_data['postal_code']
            town_city = checkout_form.cleaned_data['town_city']
            phone_number = checkout_form.cleaned_data['phone_number']
            
            if 'additional_delivery_info' in checkout_form.cleaned_data:
                additional_delivery_info = checkout_form.cleaned_data['additional_delivery_info']
            else:
                additional_delivery_info = None  #

            user = request.user
            items_in_cart = CartItem.objects.filter(user=user)
            total_price = sum(item.item.price * item.quantity for item in items_in_cart)

            order = Order.objects.create(user=user, total_price=total_price)

            delivery_info = DeliveryInformation.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                street_name=street_name,
                building_number=building_number,
                postal_code=postal_code,
                city=town_city,
                phone_number=phone_number,
                additional_delivery_info=additional_delivery_info
            )
            delivery_info.order = order  
            delivery_info.save()       
            for cart_item in items_in_cart:
                item = cart_item.item
                quantity = cart_item.quantity

                if quantity <= item.stocks:
                    OrderItem.objects.create(order=order, item=item, quantity=quantity)
                    update_stocks(item, quantity)
                    Item.objects.filter(pk=item.pk).update(quantity_sold=F('quantity_sold') + quantity)

                else:
                    return render(
                        request,
                        'checkout/checkout.html',
                        {'items_in_cart': items_in_cart, 'total_price': total_price,
                         'error_message': f'Insufficient stock for {item.name}. Please adjust the quantity or remove the item from your cart.'}
                    )

            items_in_cart.delete()

            return render(request, 'checkout/order_confirmation.html', {'order': order})
        else:
            
            items_in_cart = CartItem.objects.filter(user=request.user)
            total_price = sum(item.item.price * item.quantity for item in items_in_cart)
            return render(
                request,
                'checkout/checkout.html',
                {'items_in_cart': items_in_cart, 'total_price': total_price, 'checkout_form': checkout_form}
            )

    else:
        checkout_form = CheckoutForm()
        items_in_cart = CartItem.objects.filter(user=request.user)
        total_price = sum(item.item.price * item.quantity for item in items_in_cart)
        return render(request, 'checkout/checkout.html', {'items_in_cart': items_in_cart, 'total_price': total_price, 'checkout_form': checkout_form})

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import DeliveryInformation, Order, OrderItem
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from item.models import Item  

@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            user_id = data.get('id')
            cart_summary = data.get('cartSummary')
            delivery_info = data.get('delivery_info')
            print(cart_summary)
            user = get_object_or_404(User, id=user_id)

            delivery = DeliveryInformation.objects.create(
                user=user,
                first_name=delivery_info['firstName'],
                last_name=delivery_info['lastName'],
                street_name=delivery_info['streetName'],
                city=delivery_info['city'],
                postal_code=delivery_info['postalCode'],
                building_number=delivery_info['buildingNumber'],
                phone_number=delivery_info['phoneNumber'],
                additional_delivery_info=delivery_info['additionalDeliveryInfo']
            )

            order = Order.objects.create(user=user, total_price=0)  

            total_order_price = 0

            for item_id, item_data in cart_summary.items():
                item = get_object_or_404(Item, id=item_id)

                item_price = item_data['price']
                item_quantity = item_data['quantity']
                total_order_price += item_price * item_quantity  

                order_item = OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=item_quantity
                )

                if item.stocks >= item_quantity:
                    item.stocks -= item_quantity
                    item.quantity_sold += item_quantity
                    item.save()
                else:
                    return JsonResponse({'success': False, 'error': f'Insufficient stock for {item.name}. Please adjust the quantity or remove the item from your cart.'})

            order.total_price = total_order_price
            order.save()

            return JsonResponse({'success': True, 'message': 'Order placed successfully!', 'total_price': total_order_price})

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Failed to place order', 'exception': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

