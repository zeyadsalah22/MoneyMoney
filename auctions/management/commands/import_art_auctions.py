import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from auctions.models import Listing, Category
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Import art auction listings from CSV'

    def handle(self, *args, **options):
        file_path = 'auctions/data/art_auctions.csv'
        user_model = get_user_model()

        # Get the admin user
        User = get_user_model()
        admin_user = User.objects.get(username='admin')
        
        # Get or create 'art' category
        art_category, _ = Category.objects.get_or_create(name='artwork')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    title = row['Title']
                    price = Decimal(row['Price'])
                    image_url = row['LinkToImage']

                    listing = Listing(
                        title=title,
                        description="artwork listing.",
                        starting_price=price,
                        current_price=price,
                        category=art_category,
                        image_url=image_url,
                        seller=admin_user,
                        status=True,
                        end_date=timezone.now() + timedelta(days=7)
                    )
                    listing.save()
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to error: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Imported {count} art listings successfully."))
