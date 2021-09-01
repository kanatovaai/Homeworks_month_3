from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=5000, blank=False)
    price = models.IntegerField(default=None, blank=False)

    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True, null=True)

    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title


