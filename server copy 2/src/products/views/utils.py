from rest_framework.permissions import AllowAny
from src.products.views.base import BaseProductListView
from rest_framework.generics import RetrieveAPIView


def create_product_list_view(model_class):
    class ProductListView(BaseProductListView):
        model = model_class

    return ProductListView


def create_product_item_view(model_class, serializer_cls):
    class ProductItemView(RetrieveAPIView):
        queryset = model_class.objects.all()
        serializer_class = serializer_cls
        permission_classes = [AllowAny]

    return ProductItemView
