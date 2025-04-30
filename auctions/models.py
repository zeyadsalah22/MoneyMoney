from django.contrib.auth.models import AbstractUser
from django.db import models

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
    current_price = models.DecimalField(decimal_places=2,max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    image_url = models.URLField(blank=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE, related_name="possesion")
    status = models.CharField(default="active",max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing: {self.title}, Price: {self.current_price}"

class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="buying")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="item")
    price = models.DecimalField(decimal_places=2,max_digits=10)
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
