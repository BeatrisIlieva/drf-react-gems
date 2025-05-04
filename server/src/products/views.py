# views.py
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.products.models.characteristics.category import Category
from .models import ProductItem
from .serializers import CategorySerializer, ProductItemSerializer
from rest_framework.permissions import AllowAny


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = ProductItem.objects.all()
        paginator = ProductPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
