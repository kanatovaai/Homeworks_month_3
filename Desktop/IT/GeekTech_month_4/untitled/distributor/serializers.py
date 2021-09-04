from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import BrandCar, CarModel, Affiliate


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = 'id name'.split()


class BrandSerializer(serializers.ModelSerializer):
    # models = CarModelSerializer(many=True)
    models = serializers.SerializerMethodField()
    affiliates = serializers.SerializerMethodField()

    class Meta:
        model = BrandCar
        fields = 'id name country birthday models affiliates'.split()

    def get_models(self, brand):
        car_models = brand.models.filter(is_publish=True)
        return CarModelSerializer(car_models, many=True).data

    def get_affiliates(self, brand):
        return [i.name for i in brand.affiliates.all()]


class BrandCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    country = serializers.CharField(max_length=100)
    birthday = serializers.DateField()
    affiliates = serializers.ListField(required=True,
                                       child=serializers.IntegerField())

    def validate_name(self, name):
        print(name)
        brands = BrandCar.objects.filter(name=name)
        if brands.count() > 0:
            raise ValidationError('Такой бренд уже существует!')

    def validate_affiliates(self, affiliates):
        if Affiliate.objects.filter(id__in=affiliates).count() != len(affiliates):
            raise ValidationError('Ошибка в филиалах!')
        # for i in affiliates:
        #     try:
        #         Affiliate.objects.get(id=i)
        #     except:
        #         raise ValidationError('')


class CarMoadelCreateSrializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    brand_car_id = serializers.IntegerField()
    is_publish = serializers.BooleanField()


    def validate(self, attrs):
        id = attrs['brand_car_id']
        if BrandCar.objects.filter(id=id).count() == 0:
            raise ValidationError('Такого бренда не существует')
        return attrs


class LoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)