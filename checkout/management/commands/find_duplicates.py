# your_app/management/commands/find_duplicates.py

from django.core.management.base import BaseCommand
from django.db.models import Count
from checkout.models import DeliveryInformation  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Finds duplicate entries based on user_id in the DeliveryInformation model'

    def handle(self, *args, **options):
        # Find duplicate entries based on user_id
        duplicates = (
            DeliveryInformation.objects
            .values('user_id')
            .annotate(count_id=Count('id'))
            .filter(count_id__gt=1)
        )

        # Print duplicate entries for each user_id
        for duplicate in duplicates:
            duplicate_entries = DeliveryInformation.objects.filter(user_id=duplicate['user_id'])
            self.stdout.write(f"Duplicate entries for user_id {duplicate['user_id']}:")
            for entry in duplicate_entries:
                self.stdout.write(f"- {entry}")
