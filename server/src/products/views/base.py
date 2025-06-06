from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from src.products.serializers.type_list import ProductListSerializer


class ProductPagination(PageNumberPagination):
    page_size = 8


class BaseProductListView(ListAPIView):
    model = None
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def list(self, request, *args, **kwargs):
        data = self._get_products_data()

        page = self.paginate_queryset(data['products'])

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data.update({
                'colors': data['colors'],
                'stones': data['stones'],
                'metals': data['metals'],
                'collections': data['collections'],
            })
            return response

        serializer = self.get_serializer(data['products'], many=True)
        return Response({
            'products': serializer.data,
            'colors': data['colors'],
            'stones': data['stones'],
            'metals': data['metals'],
            'collections': data['collections'],
        })

    def _get_products_data(self):
        filters = self._get_filters()
        ordering = self.request.query_params.get('ordering', 'rating')

        if not self.model and not filters:
            return {
                'products': [],
                'colors': {},
                'stones': {},
                'collections': {},
                'metals': {},
            }

        raw_products = self.model.objects.get_product_list(filters, ordering)

        colors_by_count = self.model.objects.get_colors_by_count(raw_products)
        stones_by_count = self.model.objects.get_stones_by_count(raw_products)
        metals_by_count = self.model.objects.get_metals_by_count(raw_products)
        collections_by_count = self.model.objects.get_collections_by_count(
            raw_products)

        return {
            'products': raw_products,
            'colors': colors_by_count,
            'stones': stones_by_count,
            'collections': collections_by_count,
            'metals': metals_by_count,
        }

    def _get_filters(self):
        colors = self.request.query_params.getlist('colors')
        stones = self.request.query_params.getlist('stones')
        metals = self.request.query_params.getlist('metals')
        collections = self.request.query_params.getlist('collections')

        filters = Q()
        if colors:
            filters &= Q(color_id__in=colors)
        if stones:
            filters &= Q(stone_id__in=stones)
        if metals:
            filters &= Q(metal__id__in=metals)
        if collections:
            filters &= Q(collection__id__in=collections)

        return filters
