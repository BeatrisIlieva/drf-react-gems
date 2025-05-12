# views.py
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.products.models.characteristics.category import Category
from .models import Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 10


# class ProductListView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         products = Product.objects.all()
#         paginator = ProductPagination()
#         result_page = paginator.paginate_queryset(products, request)
#         serializer = ProductSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)


class ProductByCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        paginator = ProductPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

