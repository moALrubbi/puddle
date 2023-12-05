from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from item.models import Category, Item  # Import your models from your 'puddle' app

class Command(BaseCommand):
    help = 'Creates a custom admin group and assigns permissions for Item and Category models'

    def handle(self, *args, **options):
        # Create a new group
        item_category_admins, created = Group.objects.get_or_create(name='Item and Category Admins')

        # Get permissions for Category model
        category_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Category))
        # Assign Category permissions to the new group
        for perm in category_permissions:
            item_category_admins.permissions.add(perm)

        # Get permissions for Item model
        item_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Item))
        # Assign Item permissions to the new group
        for perm in item_permissions:
            item_category_admins.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Item and Category Admins group created with appropriate permissions.'))
