from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.exceptions import ImproperlyConfigured

from src.products.mixins import FilterMixin
from src.products.serializers.product import NeckwearSerializer, EarwearSerializer, WristwearSerializer, FingerwearSerializer
from src.products.models import Earwear, Neckwear, Wristwear, Fingerwear


class ProductPagination(PageNumberPagination):
    page_size = 8


class BaseProductListView(FilterMixin, ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    model = None
    serializer_class = None

    def get_model(self):
        if self.model is None:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} must define a `model` attribute.'
            )
        return self.model

    def get_serializer_class(self):
        if self.serializer_class is None:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} must define a `serializer_class` attribute.'
            )
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        data = self._get_products_data()
        page = self.paginate_queryset(data)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            return response

        serializer = self.get_serializer(data, many=True)

        return Response({
            'products': serializer.data,
        })

    def _get_products_data(self):
        filters = self._get_filters_for_product()
        ordering = self.request.query_params.get('ordering', 'rating')

        return self.model.objects.get_product_list(filters, ordering)


class EarwearListView(BaseProductListView):
    model = Earwear
    serializer_class = EarwearSerializer


class NeckwearListView(BaseProductListView):
    model = Neckwear
    serializer_class = NeckwearSerializer


class WristwearListView(BaseProductListView):
    model = Wristwear
    serializer_class = WristwearSerializer


class FingerwearListView(BaseProductListView):
    model = Fingerwear
    serializer_class = FingerwearSerializer
