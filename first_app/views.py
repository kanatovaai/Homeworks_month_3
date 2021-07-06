from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from first_app.models import Product, Category


def index(request):
    categories = Category.objects.all()
    data = {
        'title': 'Все категории',
        'categories': categories
    }
    return render(request, 'index.html', context=data)


def products_list(request):
    products = Product.objects.all()
    data = {
        'title': 'Все продукты',
        'products': products
    }
    return render(request, 'products.html', context=data)


def product_item(request, id):
    product = Product.objects.get(id=id)
    data = {
        'product': product
    }
    return render(request, 'products.html', context=data)
