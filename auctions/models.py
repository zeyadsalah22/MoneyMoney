from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('bidder', 'Bidder'),
        ('seller', 'Seller'),
        ('both', 'Both')
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='both'
    )

    def __str__(self):
        return f"Username: {self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    image_url = models.URLField(blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="possesion")
    status = models.BooleanField(default=True)  # True for active, False for closed
    end_date = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set current_price to starting_price if not set
        if not self.current_price:
            self.current_price = self.starting_price
        
        # Set end_date to 7 days from now if not set
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=7)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Listing: {self.title}, Current Price: {self.current_price}"

    def is_active(self):
        return self.status and self.end_date > timezone.now()

    def close_auction(self):
        if self.status:  # Only close if still active
            self.status = False
            highest_bid = self.item.order_by('-price').first()
            if highest_bid:
                self.winner = highest_bid.bidder
            self.save()

class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="buying")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="item")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} placed a bid of {self.price} for {self.listing.title}"

class Comment(models.Model):
    comment = models.TextField()
    product = models.ForeignKey(Listing,on_delete=models.CASCADE)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer.username} commented on {self.product.title}"

class WatchList(models.Model):
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing: {self.item.title} on the watchlist of {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.listing.title}"
