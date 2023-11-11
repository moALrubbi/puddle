from django.shortcuts import render, redirect
from item.models import Category, Item
from cart.models import CartItem  # Ensure to import the CartItem model from the cart app
from .forms import SignupForm
from django.contrib.auth import get_user_model

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Save the user and retrieve the created user object
            user = form.save()

            # Retrieve cart items from the session
            cart = request.session.get('cart', {})

            # Associate the cart items with the user
            for item_id, item_data in cart.items():
                item = Item.objects.get(id=item_id)
                cart_item, created = CartItem.objects.get_or_create(user=user, item=item)
                if not created:
                    cart_item.quantity = item_data['quantity']
                    cart_item.save()

            # Clear the cart from the session after associating the items with the user
            request.session['cart'] = {}

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})
