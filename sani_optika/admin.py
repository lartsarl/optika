from django.contrib import admin

from .models import User, Category, Product, Order, ProductOrder, Location, LocationSlot, Review, WishList, StarRating

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(LocationSlot)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(WishList)
admin.site.register(StarRating)

