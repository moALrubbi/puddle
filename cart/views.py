from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Cart, Item, CartItem

def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart_item = cart.get(pk, {'quantity': 0})
        cart_item['quantity'] += 1
        cart[pk] = cart_item
        request.session['cart'] = cart

    return redirect('item:detail', pk=pk)

def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user_cart = get_object_or_404(Cart, user=request.user)
    user_cart.items.remove(item)
    # Increase the item's stocks in the database when removed from the cart
    return redirect('cart_items')

def cart_items(request):
    if request.user.is_authenticated:
        items_in_cart = CartItem.objects.filter(user=request.user)
        total_price = sum(item.item.price * item.quantity for item in items_in_cart)
        return render(request, 'cart/cart_items.html', {'items_in_cart': items_in_cart, 'total_price': total_price})
    else:
        # Anonymous user handling
        if request.method == 'POST':
            pk = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity'))
            cart = request.session.get('cart', {})
            cart_item = cart.get(pk)
            if cart_item:
                cart_item['quantity'] = quantity
                request.session['cart'] = cart

        cart = request.session.get('cart', {})
        items_in_cart = []
        total_price = 0
        for pk, cart_item in cart.items():
            item = get_object_or_404(Item, pk=pk)
            total_price += item.price * cart_item['quantity']
            items_in_cart.append({'item': item, 'quantity': cart_item['quantity']})

        return render(request, 'cart/cart_items.html', {'items_in_cart': items_in_cart, 'total_price': total_price})

def update_quantity(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            quantity = int(request.POST['quantity'])
            item = get_object_or_404(Item, pk=pk)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
        else:
            quantity = int(request.POST['quantity'])
            item_id = int(pk)
            cart = request.session.get('cart', {})
            if str(item_id) in cart:
                cart[str(item_id)]['quantity'] = quantity
                request.session['cart'] = cart

    return redirect('cart_items')

User = get_user_model()
