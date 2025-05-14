from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.serializers import ProductListSerializer
from src.products.models.product import Product


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()
