# your_app/management/commands/remove_duplicates.py

from django.core.management.base import BaseCommand
from checkout.models import DeliveryInformation  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Remove duplicate entries in DeliveryInformation'

    def handle(self, *args, **kwargs):
        # Find duplicate entries for user_id=1
        duplicates = (
            DeliveryInformation.objects
            .filter(user_id=1)
            .order_by('id')
        )

        # Keep the first entry and delete the rest
        for index, duplicate in enumerate(duplicates):
            if index > 0:
                duplicate.delete()

        self.stdout.write(self.style.SUCCESS('Duplicate entries removed successfully.'))
