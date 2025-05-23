from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.products.serializers import ProductListSerializer
from src.products.models.base import Product


class ProductPagination(PageNumberPagination):
    page_size = 6


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_products_data(self):
        category_id = self.request.query_params.get('category')
        color_ids = self.request.query_params.getlist('color_ids')
        stone_ids = self.request.query_params.getlist('stone_ids')
        material_ids = self.request.query_params.getlist('material_ids')

        filters = Q()
        if category_id:
            filters &= Q(category_id=category_id)

        if color_ids:
            filters &= Q(stone_by_color__color_id__in=color_ids)
        if stone_ids:
            filters &= Q(stone_by_color__stone_id__in=stone_ids)
        if material_ids:
            filters &= Q(material__id__in=material_ids)

        if filters:
            return Product.objects.get_products(filters)
        return {'products': [], 'colors_by_count': {}, 'stones_by_count': {}, 'materials_by_count': {}, 'price_ranges': {}}

    def list(self, request, *args, **kwargs):
        data = self.get_products_data()

        page = self.paginate_queryset(data['products'])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['colors_by_count'] = data['colors_by_count']
            paginated_response.data['stones_by_count'] = data['stones_by_count']
            paginated_response.data['materials_by_count'] = data['materials_by_count']
            paginated_response.data['price_ranges'] = data['price_ranges']
            return paginated_response

        serializer = self.get_serializer(data['products'], many=True)
        return Response({
            'products': serializer.data,
            'colors_by_count': data['colors_by_count'],
            'stones_by_count': data['stones_by_count'],
            'materials_by_count': data['materials_by_count'],
            'price_ranges': data['price_ranges'],
        })


# class CategoryListView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [AllowAny]
