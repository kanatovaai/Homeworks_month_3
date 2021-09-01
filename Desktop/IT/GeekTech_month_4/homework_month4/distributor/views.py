from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Category, Tag

# Create your views here.)
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer, CategorySerializer, TagSerializer, ProductCreateSerializer, \
    LoginValidateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_rest_view(request):
    if request.method == "GET":
        print(request.user)
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        title = request.data['title']
        description = request.data['description']
        price = request.data['price']
        product = Product.objects.create(
            title=title, description=description, price=price
        )
        category = request.data['category']
        product.category_id = category
        product.save()
        tags = request.data['tags']
        for i in tags:
            product.tags.add(i)
        product.save()
        return Response(data={'message': 'New product created!',
                              'product': ProductSerializer(product).data})


@api_view(['GET', 'PUT'])
def product_item_rest_view(request, id):
    try:
        products = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product does not exists!!!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        products.title = request.data['title']
        products.description = request.data['description']
        products.price = request.data['price']
        products.category_id = request.data['category']
        products.save()
        for i in request.data['tags']:
            products.tags.add(i)
        products.save()

    data = ProductSerializer(products).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def category_list_rest_view(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_item_rest_view(request, id):
    categories = Category.objects.get(id=id)
    print('name:', categories.name)
    print('products:', categories.products.all())
    data = CategorySerializer(categories).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def tags_list_rest_api(request):
    tags = Tag.objects.all()
    data = TagSerializer(tags, many=True).data
    return Response(data=data)


@api_view(['GET'])
def tags_item_rest_api(request, id):
    tags = Tag.objects.get(id=id)
    data = TagSerializer(tags).data
    return Response(data=data)

from django.contrib import auth

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data = {
                    'message': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user = auth.authenticate(**serializer.validated_data)
        if user:
            try:
                token = Token.objects.get(user=user)
                print('GET TOKEN')
            except Token.DoesNotExist:
                print('CREATE TOKEN')
                token = Token.objects.get(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(
                data={'message': 'Такого пользователя не существует!!!'},
                status=status.HTTP_404_NOT_FOUND
            )