from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Unique ID for each product
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Field to store product image
    product_name = models.CharField(max_length=255, null=False)  # Name of the product
    category = models.CharField(max_length=100, blank=True, null=True)  # Category of the product
    description = models.TextField(blank=True, null=True)  # Description of the product
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when product was added

    def __str__(self):
        return self.product_name


# Review Model
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    ip_address = models.CharField(max_length=50)  # Store the IP address as a string
    sentiment_label = models.CharField(max_length=50, null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    is_fake = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.product_name}'
