from rest_framework import serializers

from favourites.models import FavouriteNews, FavouriteLegislation
from .models import News, ImageNews, Legislation


class NewsListSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = 'id title short_description created_at image is_favourite'.split()

    def get_is_favourite(self, news):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return bool(FavouriteNews.objects.filter(user=user, news_id=news.id).count() > 0)


class NewsItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = 'id title full_description link images'.split()

    def get_images(self, news):
        images = ImageNews.objects.filter(news=news)
        return [i.image.url for i in images]


class LegislationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = 'id title short_description'.split()

    def get_is_favourite(self, news):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return bool(FavouriteLegislation.objects.filter(user=user, news_id=news.id).count() > 0)


class LegislationItemSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Legislation
        fields = 'id title full_description is_favourite'
