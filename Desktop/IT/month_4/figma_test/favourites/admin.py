from django.contrib import admin

# Register your models here.
from favourites.models import FavouriteNews, FavouriteLegislation


admin.site.register(FavouriteNews)
admin.site.register(FavouriteLegislation)
