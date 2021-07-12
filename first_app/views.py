import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .forms import ProductCreateForm, ReviewCreateForm, UserRegisterForm
from .models import Product, Category, Review


def index(request):
    print(request.user)
    categories = Category.objects.all()
    data = {
        'title': 'Все категории',
        'categories': categories
    }
    return render(request, 'index.html', context=data)


def category_item(request, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category_id=id)
    data = {
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context=data)


def product_item(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product_id=id)
    data = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'products.html', context=data)


def product_list(request):
    text = request.GET.get('search_text', '')
    products = Product.objects.filter(title__contains=text)
    try:
        price = int(request.GET.get('price'))
        products = products.filter(price=price)
    except:
        pass
    category = request.GET.get('category', '')
    if category != '':
        products = products.filter(category_id=int(category))
    return render(request, 'all_products.html', context={
        'products': products,
        'categories': Category.objects.all()
    })


@login_required(login_url='/login/')
def add_product(request):
    if request.method == 'GET':
        print('GET')
        form = ProductCreateForm()
        data = {
            'form': form
        }
        return render(request, 'add_product.html',
                      context=data)
    elif request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
        else:
            return render(request, 'add_product.html',
                          context={'form': form})


@login_required(login_url='/login/')
def add_review(request):
    if request.method == 'GET':
        print('GET')
        form = ReviewCreateForm()
        data = {
            'form': form
        }
        return render(request, 'add_review.html',
                      context=data)
    elif request.method == 'POST':
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
        else:
            return render(request, 'add_review.html',
                          context={'form': form})


from django.contrib import auth


def login(request):
    data = {}
    next = (request.GET.get('next'))
    if next:
        data['message'] = 'Авторизуйтесь, чтобы добавить.'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            data['message'] = 'Введите правильные данные!'
    return render(request, 'login.html', context=data)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST['email'],
                password=request.POST['password'],
                is_active=False
            )
            send_mail(
                subject='ORGANIC FOOD',
                message='Добро пожаловать в магазин ORGANIC FOOD!'
                        'Благодарим Вас за регистрацию!',
                from_email=settings.EMAIL_HOST,
                recipient_list=[request.POST['email']]
            )
        else:
            return render(request, 'register.html', context={
                'form': form
            })
    data = {
        'form': UserRegisterForm()
    }
    return render(request, 'register.html', context=data)


def product_count(request):
    count = Product.objects.all().count()
    return JsonResponse(data={'count': count})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        text = json.loads(request.body).get('search_text', '')
        products = Product.objects.filter(title__contains=text)
        return JsonResponse(data=list(products.values()), safe=False)


def search_product(request):
    return render(request, 'search.html')