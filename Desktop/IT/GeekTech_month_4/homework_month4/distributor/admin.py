from django.contrib import admin
from distributor.models import Category, Tag, Product


# Register your models here.


class ProductModelInLine(admin.StackedInline):
    model = Product
    extra = 0

class CategoryModelInLine(admin.StackedInline):
    model = Category
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

    inlines = [ProductModelInLine]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Product)
