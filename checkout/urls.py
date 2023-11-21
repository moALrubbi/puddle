# checkout/urls.py

from django.urls import path
from .views import checkout,place_order
from . import views

urlpatterns = [
    path('', checkout, name='checkout'),
    path('api/place_order/', place_order, name='place_order'),  # Define the URL pattern for place_order

]
