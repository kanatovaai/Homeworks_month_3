from django.shortcuts import render
from .serializers import NewsListSerializer, NewsItemSerializer, LegislationListSerializer, LegislationItemSerializer
from .models import News, ImageNews, Legislation
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


# from fpdf import FPDF


# Create your views here.


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_queryset(),
                                     many=True,
                                     context={'request': request}).data
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)


class NewsItemAPIView(generics.RetrieveAPIView):
    serializer_class = NewsItemSerializer
    queryset = News.objects.all()


class LegislationListAPIVIew(generics.ListAPIView):
    queryset = Legislation.objects.all()
    serializer_class = LegislationListSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_queryset(),
                                     many=True,
                                     context={'request': request}).data
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)


#  для сслыки PDF файла
# def index(request):
#     context = {}
#     return render(request, "index.html", context=context)
#
#
# def pdf_file():
#     return None


class LegislationItemAPIVIew(generics.RetrieveAPIView):
    serializer_class = LegislationItemSerializer
    queryset = Legislation.objects.all()
