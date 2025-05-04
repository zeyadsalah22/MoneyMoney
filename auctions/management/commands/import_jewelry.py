from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from auctions.models import Listing, Category
import requests
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Import jewelry listings from Etsy API'

    def handle(self, *args, **options):
        # Get or create the Jewelry category
        category, created = Category.objects.get_or_create(
            name="Jewelries",
            defaults={'description': 'Beautiful jewelry pieces from around the world'}
        )

        # Get the admin user
        User = get_user_model()
        admin_user = User.objects.get(username='admin')

        # Etsy API endpoint for jewelry listings
        # Note: In a real implementation, you would need to register for an Etsy API key
        # For this example, we'll use mock data
        jewelry_data = [
            {
                'title': 'Platinum Wedding Band',
                'description': 'Solid platinum band with brushed finish. A luxurious choice for a wedding or anniversary.',
                'starting_price': 950.00,
                'image_url': 'https://images.unsplash.com/photo-1605521841547-803b1cd6f1c5?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Vintage Opal Ring',
                'description': 'Antique-style ring featuring an oval opal and intricate engravings. A unique vintage find.',
                'starting_price': 520.00,
                'image_url': 'https://images.unsplash.com/photo-1611175035856-0cbb499ff7a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Rose Gold Bangle',
                'description': 'Minimalist 18K rose gold bangle with a polished finish. Stylish and stackable.',
                'starting_price': 280.00,
                'image_url': 'https://images.unsplash.com/photo-1621263728455-54f2f3dd5f0e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Turquoise Beaded Necklace',
                'description': 'Handcrafted necklace with natural turquoise beads. Great for a boho-chic look.',
                'starting_price': 130.00,
                'image_url': 'https://images.unsplash.com/photo-1599944652650-8e646e62f0e7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Men’s Titanium Bracelet',
                'description': 'Durable and sleek titanium bracelet with magnetic clasp. Designed for modern men.',
                'starting_price': 180.00,
                'image_url': 'https://images.unsplash.com/photo-1564314968609-5241cfd1e837?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Custom Name Necklace',
                'description': 'Personalized 14K gold necklace featuring your name or a meaningful word.',
                'starting_price': 190.00,
                'image_url': 'https://images.unsplash.com/photo-1620665272519-25c69a76cf0a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Black Onyx Ring',
                'description': 'Bold ring featuring a polished black onyx stone set in sterling silver.',
                'starting_price': 320.00,
                'image_url': 'https://images.unsplash.com/photo-1606813909047-6ee00e28ff99?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Crystal Charm Bracelet',
                'description': 'Silver bracelet with colorful Swarovski crystal charms. Fun and eye-catching.',
                'starting_price': 140.00,
                'image_url': 'https://images.unsplash.com/photo-1612170871997-0b942e2f43d9?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Amethyst Drop Pendant',
                'description': 'Beautiful 14K white gold pendant with a teardrop-shaped amethyst. Elegant and calming.',
                'starting_price': 410.00,
                'image_url': 'https://images.unsplash.com/photo-1593467608743-f75b62d64224?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            },
            {
                'title': 'Leather and Gold Bracelet',
                'description': 'Brown leather bracelet with 18K gold accents. Great for casual or business wear.',
                'starting_price': 230.00,
                'image_url': 'https://images.unsplash.com/photo-1610962749943-d389273ecf1a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
            }
        ]

        # Create listings
        for item in jewelry_data:
            # Generate a random end date between 7 and 30 days from now
            end_date = datetime.now() + timedelta(days=random.randint(7, 30))
            
            listing = Listing.objects.create(
                title=item['title'],
                description=item['description'],
                starting_price=item['starting_price'],
                current_price=item['starting_price'],
                image_url=item['image_url'],
                category=category,
                seller=admin_user,
                end_date=end_date,
                status=True  # Active listing
            )
            self.stdout.write(self.style.SUCCESS(f'Created listing: {listing.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported jewelry listings')) 