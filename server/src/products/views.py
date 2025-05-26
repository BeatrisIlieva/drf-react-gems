from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from decimal import Decimal
from src.products.models.review import Review
from src.products.serializers import EarwearSerializer, FingerwearSerializer, NeckwearSerializer, ProductListSerializer, ReviewSerializer, WristwearSerializer

from src.products.models.earwear import Earwear
from src.products.models.fingerwear import Fingerwear
from src.products.models.neckwear import Neckwear
from src.products.models.wristwear import Wristwear


class ProductPagination(PageNumberPagination):
    page_size = 8


class BaseProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    model = None

    def _get_filters(self):
        color_ids = self.request.query_params.getlist('color_ids')
        stone_ids = self.request.query_params.getlist('stone_ids')
        material_ids = self.request.query_params.getlist('material_ids')
        collection_ids = self.request.query_params.getlist('collection_ids')
        category_ids = self.request.query_params.getlist('category_ids')
        min_price = self.request.query_params.getlist('min_price')
        max_price = self.request.query_params.getlist('max_price')

        filters = Q()
        if color_ids:
            filters &= Q(stone_by_color__color_id__in=color_ids)
        if stone_ids:
            filters &= Q(stone_by_color__stone_id__in=stone_ids)
        if material_ids:
            filters &= Q(material__id__in=material_ids)
        if collection_ids:
            filters &= Q(collection__id__in=collection_ids)
        if category_ids:
            filters &= Q(reference__id__in=category_ids)
        if min_price:
            filters &= Q(price__gt=Decimal(min_price[0]))
        if max_price:
            filters &= Q(price__lt=Decimal(max_price[0]))

        return filters

    def _get_products_data(self):
        filters = self._get_filters()
        if not self.model and not filters:
            return {
                'products': [],
                'colors_by_count': {},
                'stones_by_count': {},
                'collections_by_count': {},
                'categories_by_count': {},
                'materials_by_count': {},
                'price_ranges': {},
            }

        return self.model.objects.get_products(filters)

    def list(self, request, *args, **kwargs):
        data = self._get_products_data()
        page = self.paginate_queryset(data['products'])

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data.update({
                'colors_by_count': data['colors_by_count'],
                'stones_by_count': data['stones_by_count'],
                'materials_by_count': data['materials_by_count'],
                'collections_by_count': data['collections_by_count'],
                'categories_by_count': data['categories_by_count'],
                'price_ranges': data['price_ranges'],
            })
            return response

        serializer = self.get_serializer(data['products'], many=True)
        return Response({
            'products': serializer.data,
            'colors_by_count': data['colors_by_count'],
            'stones_by_count': data['stones_by_count'],
            'materials_by_count': data['materials_by_count'],
            'collections_by_count': data['collections_by_count'],
            'categories_by_count': data['categories_by_count'],
            'price_ranges': data['price_ranges'],
        })


class EarwearListView(BaseProductListView):
    model = Earwear


class FingerwearListView(BaseProductListView):
    model = Fingerwear


class NeckwearListView(BaseProductListView):
    model = Neckwear


class WristwearListView(BaseProductListView):
    model = Wristwear


class EarwearItemView(RetrieveAPIView):
    queryset = Earwear.objects.all()
    serializer_class = EarwearSerializer
    permission_classes = [AllowAny]


class FingerwearItemView(RetrieveAPIView):
    queryset = Fingerwear.objects.all()
    serializer_class = FingerwearSerializer
    permission_classes = [AllowAny]


class NeckwearItemView(RetrieveAPIView):
    queryset = Neckwear.objects.all()
    serializer_class = NeckwearSerializer
    permission_classes = [AllowAny]


class WristwearItemView(RetrieveAPIView):
    queryset = Wristwear.objects.all()
    serializer_class = WristwearSerializer
    permission_classes = [AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    # GET /api/reviews/?content_type=7&object_id=123
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        content_type_id = self.request.query_params.get('content_type_id')
        object_id = self.request.query_params.get('object_id')

        if content_type_id and object_id:
            queryset = queryset.filter(
                content_type_id=content_type_id, object_id=object_id)
        return queryset
