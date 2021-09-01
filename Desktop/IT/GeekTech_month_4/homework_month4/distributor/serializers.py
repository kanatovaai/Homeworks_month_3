from django.db.models import IntegerField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id title description price tags'.split()


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products'.split()

    def get_products(self, category):
        product = category.products.filter(is_publish=True)
        return ProductSerializer(product, many=True).data


class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.ListField(required=True,
                                 child=serializers.IntegerField())

    def validate_title(self, title):
        product = Product.objects.filter(title=title)
        if product.count() > 0:
            raise ValidationError('Такой пордукт уже существует!!!')

    def validate_tags(self, tags):
        if Tag.objects.filter(id__in=tags).count() != len(tags):
            raise ValidationError('Ошибка в тегах!')


class LoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
