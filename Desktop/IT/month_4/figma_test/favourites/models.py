from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from distributor.models import News, Legislation


class FavouriteNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FavouriteLegislation(models.Model):
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)