from django.db import models
from datetime import datetime, date

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=60, blank=False)
    username = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=60, blank=False)
    address = models.CharField(max_length=60, blank=False)
    is_admin = models.BooleanField(default=False)
    coupons = models.FloatField(default=0, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False)
    deleted = models.BooleanField(default=False)

class Product(models.Model):
    name = models.CharField(max_length=30, blank=False)
    price = models.FloatField(default=0, blank=False)
    image_path = models.CharField(max_length=200, blank=True)
    rating = models.FloatField(default=0)
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

class Review(models.Model):
    path = models.CharField(max_length=200)
    text = models.CharField(max_length=200, default="")
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=False,on_delete=models.CASCADE)

class Order(models.Model):
    datetime = models.DateTimeField(default=datetime.now)
    total = models.FloatField(default=0, blank=False)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

class ProductOrder(models.Model):
    quantity = models.PositiveIntegerField(default=1, blank=False)
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, default=None)
    order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE, default=None)

class Location(models.Model):
    city = models.CharField(max_length=60, blank=False)
    address = models.CharField(max_length=60, blank=False)

class LocationSlot(models.Model):
    date = models.DateField(default=datetime.now)
    starts = models.CharField(max_length=10, blank=False)
    location = models.ForeignKey(Location, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

class WishList(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, default=None)

class StarRating(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, default=None)
    stars = models.PositiveIntegerField(default=1, blank=False)
    