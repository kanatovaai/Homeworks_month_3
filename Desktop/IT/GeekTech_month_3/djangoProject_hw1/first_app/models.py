from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(default=12, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=200, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text
