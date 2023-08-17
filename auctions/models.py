from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"Username: {self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.DecimalField(decimal_places=2,max_digits=10)
    category = models.CharField(blank=True, max_length=64)
    image_url = models.URLField(blank=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE, related_name="possesion")
    status = models.CharField(default="active",max_length=64)
    def __str__(self):
        return f"Listing: {self.title}, Price: {self.current_price}"

class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="buying")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="item")
    price = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.bidder.username} placed a bid of {self.price} for {self.listing.title}"

class Comment(models.Model):
    comment = models.TextField()
    product = models.ForeignKey(Listing,on_delete=models.CASCADE)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.writer.username} commented on {self.product.title}"

class WatchList(models.Model):
    item = models.ForeignKey(Listing,on_delete=models.CASCADE )
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing: {self.item.title} on the watchlist of {self.user.username}"
