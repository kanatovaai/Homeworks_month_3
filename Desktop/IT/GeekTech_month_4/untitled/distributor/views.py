from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import BrandCar, CarModel, Affiliate


# Create your views here.
from .permissions import IsAdmin


def brand_list_view(request):
    brands = BrandCar.objects.all()
    brand_list = []
    for i in brands:
        brand_list.append(
            {
                'id': i.id,
                'name': i.name,
                'country': i.country,
                'birthday': i.birthday,
            }
        )
    data = {
        'brands': brand_list
    }
    return JsonResponse(data=data, safe=False)


from rest_framework.decorators import api_view, permission_classes
from .serializers import BrandSerializer, BrandCreateSerializer, CarMoadelCreateSrializers, LoginValidateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def brand_list_rest_view(request):
    if request.method == "GET":
        print(request.user)
        brands = BrandCar.objects.all()
        data = BrandSerializer(brands, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = BrandCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        name = request.data['name']
        country = request.data['country']
        birthday = request.data['birthday']
        brand = BrandCar.objects.create(
            name=name, country=country, birthday=birthday
        )
        affiliates = request.data['affiliates']
        for i in affiliates:
            brand.affiliates.add(i)
        brand.save()
        return Response(data={'message': 'OK',
                              'brand': BrandSerializer(brand).data})


@api_view(['GET', 'PUT'])
def brand_item_rest_view(request, id):
    try:
        brands = BrandCar.objects.get(id=id)
    except BrandCar.DoesNotExist:
        return Response(data={'message': 'Brand does not exists!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        brands.name = request.data['name']
        brands.country = request.data['country']
        brands.birthday = request.data['birthday']
        brands.affiliates.clear()
        for i in request.data['affiliates']:
            brands.affiliates.add(i)
        brands.save()
    data = BrandSerializer(brands).data
    return Response(data=data)


@api_view(['POST'])
def test(request):
    name = request.data.get('name', 'China')
    Affiliate.objects.create(name=name)
    return Response(data={'message': 'received'})


@api_view(['POST'])
@permission_classes([IsAdmin])
def car_models_view(request):
    serializer = CarMoadelCreateSrializers(data=request.data)
    if not serializer.is_valid():
        return Response(data={
            'message': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    # car = CarModel.objects.create(
    #     name=request.data['name'],
    #     brand_car_id=request.data['brand_car_id'],
    #     is_publish=request.data['is_publish']
    # )

    CarModel.objects.create(**serializer.validated_data)

    return Response()


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
            except Token.DoesNotExist:
                token = Token.objects.get(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(
                data={'message': 'User is not found!!!'},
                status=status.HTTP_404_NOT_FOUND
            )
