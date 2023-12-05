
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Adds a user to the Item and Category Admins group'

    def handle(self, *args, **options):
        # Retrieve the user
        user = User.objects.get(username='alrubbi')  # Replace 'example_user' with the actual username

        # Retrieve the 'Item and Category Admins' group
        item_category_admins_group = Group.objects.get(name='Item and Category Admins')

        # Add the user to the group
        user.groups.add(item_category_admins_group)
        self.stdout.write(self.style.SUCCESS(f"User '{user.username}' added to the group."))
