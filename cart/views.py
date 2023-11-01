# cart/views.py
from django.shortcuts import render,get_object_or_404, redirect
from .models import Cart, Item
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Item





def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)  # Retrieve the item by its primary key
    
    # Get or create the cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Add the item to the cart
    cart.items.add(item)
    
    # Optionally, you can add a success message
    # messages.success(request, f"{item.name} added to cart.")
    
    return redirect('item:detail', pk=pk) 


# cart/views.py


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user_cart = get_object_or_404(Cart, user=request.user)
    
    user_cart.items.remove(item)  # Remove the item from the cart

    return redirect('cart_items')  # Ensure the name 'cart_items' matches the URL pattern name in your urls.py


def cart_items(request):
    user_cart = get_object_or_404(Cart, user=request.user)
    items_in_cart = user_cart.items.all()

    return render(request, 'cart/cart_items.html', {'items_in_cart': items_in_cart})