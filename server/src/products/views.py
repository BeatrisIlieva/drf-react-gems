from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.models.relationships.category import Category
from src.products.serializers import CategorySerializer, ProductListSerializer
from src.products.models.product import Product

class ProductPagination(PageNumberPagination):
    page_size = 8


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        qs = Product.objects.all()

        if category_id:
            qs = qs.filter(category_id=category_id)

        return (
            qs
            .order_by('first_image', 'created_at')
            .distinct('first_image')
            .select_related('first_image', 'size', 'reference')
        )


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
