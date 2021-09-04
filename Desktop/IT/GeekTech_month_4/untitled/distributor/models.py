from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Affiliate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BrandCar(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birthday = models.DateField()
    affiliates = models.ManyToManyField(Affiliate,
                                        blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    brand_car = models.ForeignKey(BrandCar, related_name='models',
                                  on_delete=models.CASCADE)
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.name


CLIENT = 1
COURIER = 2
ADMIN = 3

ROLES = (
    (CLIENT, 'CLIENT'),
    (COURIER, 'COURIER'),
    (ADMIN, 'ADMIN'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    role = models.IntegerField(choices=ROLES)

    def __str__(self):
        return self.user.username
