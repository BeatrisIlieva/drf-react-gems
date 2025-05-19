from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.models.relationships.category import Category
from src.products.serializers import CategorySerializer, ProductListSerializer
from src.products.models.product_item import ProductItem


class ProductPagination(PageNumberPagination):
    page_size = 6


# class ProductListView(ListAPIView):
#     serializer_class = ProductListSerializer
#     permission_classes = [AllowAny]
#     pagination_class = ProductPagination

#     def get_queryset(self):
#         category_id = self.request.query_params.get('category')
#         color_id = self.request.query_params.getlist('color')

#         filters = Q()
#         if category_id:
#             filters &= Q(category_id=category_id)
#         if color_id:
#             filters &= Q(stone_by_color__color_id__in=color_id)

#         if filters:
#             products_data = ProductItem.objects.get_products(filters)
#         else:
#             products_data = []

#         return products_data


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_products_data(self):
        category_id = self.request.query_params.get('category')
        color_id = self.request.query_params.getlist('color')

        filters = Q()
        if category_id:
            filters &= Q(category_id=category_id)
        if color_id:
            filters &= Q(stone_by_color__color_id__in=color_id)

        if filters:
            return ProductItem.objects.get_products(filters)
        return {'products': [], 'colors_by_count': {}, 'stones_by_count': {}}

    def list(self, request, *args, **kwargs):
        # Get the full data (products and color stats)
        data = self.get_products_data()

        # Paginate only the product list
        page = self.paginate_queryset(data['products'])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['colors_by_count'] = data['colors_by_count']
            paginated_response.data['stones_by_count'] = data['stones_by_count']
            return paginated_response

        # If pagination is not applied
        serializer = self.get_serializer(data['products'], many=True)
        return Response({
            'products': serializer.data,
            'colors_by_count': data['colors_by_count'],
            'stones_by_count': data['stones_by_count']
        })



class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
