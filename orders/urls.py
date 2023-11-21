# orders/urls.py

from django.urls import path
from . import views
from .views import user_orders_api_view

urlpatterns = [
    path('', views.user_orders, name='user_orders'),  # URL for displaying user orders
    path('api/orders/', views.orders_api_view, name='orders-api'),
    path('api/user-orders/<int:user_id>/', user_orders_api_view, name='user_orders_api'),

]
