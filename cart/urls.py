from django.urls import path
from . import views

from .views import cart_items,add_to_cart # Import the view function

urlpatterns = [
    path('<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_items, name='cart_items'),  # Define the cart items view without /cart
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),  # URL for removing items from the cart
    path('cart/', views.cart_items, name='cart'),
    path('', cart_items, name='cart'),  # Define the URL path for cart
    # Other URL patterns for the cart app if present
]
