# puddle/item/custom_admin.py

from django.contrib.admin import AdminSite
from .models import Category, Item

class CustomAdminSite(AdminSite):
    site_header = 'Custom Admin Panel'
    site_title = 'Custom Admin Panel'
    index_title = 'Welcome to the Custom Admin Panel'


custom_admin_site = CustomAdminSite(name='admin2')
custom_admin_site.register(Category)
custom_admin_site.register(Item)
