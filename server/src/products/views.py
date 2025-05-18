from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.models.relationships.category import Category
from src.products.serializers import CategorySerializer, ProductListSerializer
from src.products.models.product_item import ProductItem


class ProductPagination(PageNumberPagination):
    page_size = 6


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        category_id = self.request.query_params.get('category')

        if category_id:
            products_data = ProductItem.objects.get_products(
                category_id=category_id)
        else:
            products_data = []

        return products_data


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
