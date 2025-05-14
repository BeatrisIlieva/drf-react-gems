from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.models.relationships.category import Category
from src.products.serializers import CategorySerializer, ProductListSerializer
from src.products.models.product import Product


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
