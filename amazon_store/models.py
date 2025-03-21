from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
# from datetime import datetime, timedelta

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Product Model


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image2 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image3 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image4 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image5 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    reviews = models.IntegerField(default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)  # Percentage discount
    delivery_date = models.DateField(default=timezone.now)  # <-- Add default value here


    def calculate_discount(self):
        if self.original_price and self.discounted_price:
            self.discount = int(((self.original_price - self.discounted_price) / self.original_price) * 100)
            self.save()


    def __str__(self):
        return self.title

# Cart Model
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def calculate_price(self):
        self.price = self.product.price * self.quantity
        self.save()

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

# Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order of {self.product.title} (x{self.quantity})"



# adress model
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)




# wishlist
class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries
        
    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.title}"
    