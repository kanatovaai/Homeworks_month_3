from django.contrib import admin
from distributor.models import BrandCar, CarModel, Affiliate, Profile


# Register your models here.
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 0


class BrandAdmin(admin.ModelAdmin):
    class Meta:
        model = BrandCar
    inlines = [CarModelInline]


admin.site.register(BrandCar, BrandAdmin)
admin.site.register(CarModel)
admin.site.register(Affiliate)
admin.site.register(Profile)