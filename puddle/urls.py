#puddle/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from item.custom_admin import custom_admin_site  # Import your custom admin site

urlpatterns = [
    path('', include('core.urls')),
    path('items/', include('item.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('conversation.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),  # Include the URLs from the cart app
    path('checkout/', include('checkout.urls')),  # Add this line
    path('orders/', include('orders.urls')),  # Include URLs for the "orders" app
    path('admin2/', custom_admin_site.urls),  # Change 'admin2/' to your desired admin URL

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
