# Create a custom Django management command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from checkout.models import DeliveryInformation, Order

class Command(BaseCommand):
    help = 'Creates a custom admin group and assigns permissions for Checkout models and views'

    def handle(self, *args, **options):
        checkout_admins, created = Group.objects.get_or_create(name='Checkout Admins')

        delivery_info_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(DeliveryInformation))
        for perm in delivery_info_permissions:
            checkout_admins.permissions.add(perm)

        order_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Order))
        for perm in order_permissions:
            checkout_admins.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Checkout Admins group created with appropriate permissions.'))
