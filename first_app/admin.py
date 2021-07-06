from django.contrib import admin

# Register your models here.
from first_app.models import Category, Product, Review


class ProductInLine(admin.StackedInline):
    model = Product
    fields = 'title price'.split()
    extra = 1


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'text product'.split()
    list_filter = 'product'.split()


class ProductAdmin(admin.ModelAdmin):
    list_display = 'title description price category'.split()
    search_fields = 'title '.split()
    list_filter = 'price category'.split()


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
