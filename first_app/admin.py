from django.contrib import admin

# Register your models here.
from first_app.models import Category, Product, Review


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)

