import json
from django.shortcuts import render, redirect
from item.models import Category, Item
from cart.models import CartItem  # Ensure to import the CartItem model from the cart app
from .forms import SignupForm
from django.contrib.auth import get_user_model
from django.http import JsonResponse

def index(request):
    items = Item.objects.filter(is_sold=False)[0:]
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

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Get JSON data from the request body
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            # Retrieve fields from JSON data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirmPassword = data.get('confirmPassword')

            print(f"Username: {username}, Email: {email}, Password: {password}")


            # Validate user input
            if not (username and email and password and confirmPassword):
                return JsonResponse({'success': False, 'error': 'Please provide all required fields'})
            if password != confirmPassword:
                return JsonResponse({'success': False, 'error': 'Passwords do not match'})

            # Check if the email address is already in use
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email address is already in use'})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Additional actions if needed upon successful signup
            # For example: login the user automatically after signup
            
            return JsonResponse({'success': True, 'message': 'User signed up successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Signup failed', 'exception': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
# Other Django views...


from django.shortcuts import render
from item.models import Item

def statistics(request):
    # Get top 3 items based on the quantity sold
    top_items = Item.objects.order_by('-quantity_sold')[:3]  # Replace 'quantity_sold' with your field that tracks sales

    return render(request, 'core/statistics.html', {'top_items': top_items})


def statistics_api_view(request):
    # Get top 3 items based on the quantity sold
    top_items = Item.objects.order_by('-quantity_sold')[:3]  # Replace 'quantity_sold' with your field that tracks sales

    # Serialize statistics data (convert to JSON or desired format)
    top_items_data = [
        {
            'name': item.name,
            'quantity_sold': item.quantity_sold,
            'image_url': request.build_absolute_uri(item.image.url) if item.image else None,
            'price': item.price,
            'description': item.description,
            # Include other item details as needed
        }
        for item in top_items
    ]

    # Return statistics data as JSON response
    return JsonResponse({'top_items': top_items_data})


from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            # Get JSON data from the request body
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            # Retrieve username and password from JSON data
            username = data.get('username')
            password = data.get('password')
            print(f"Username: {username}, Password: {password}")

            # Validate user input
            if not (username and password):
                return JsonResponse({'success': False, 'error': 'Please provide username and password'})

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User authentication successful
                return JsonResponse({
                    'success': True,
                    'message': 'User logged in successfully!',
                    'username': user.username,
                    'id': user.id 
                })
            else:
                # Invalid credentials
                return JsonResponse({'success': False, 'error': 'Invalid username or password'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Login failed', 'exception': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.contrib.auth.models import User
from django.http import JsonResponse

def get_user(request):
    # Retrieve all users from the database
    users = User.objects.all()

    # Extract usernames and hashed passwords and create a dictionary
    user_credentials = [{'username': user.username, 'id': user.id} for user in users]

    # Return user credentials as a JSON response
    return JsonResponse({'user_credentials': user_credentials})
