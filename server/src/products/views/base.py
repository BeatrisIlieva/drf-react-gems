from typing import Any
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.response import Response as DRFResponse


from src.products.mixins import FilterMixin


class BaseProductView(APIView):
    permission_classes: list[type[AllowAny]] = [AllowAny]


class ProductPagination(PageNumberPagination):
    page_size: int = 8


class BaseProductListView(FilterMixin, ListAPIView, BaseProductView):
    pagination_class = ProductPagination

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> DRFResponse:
        data = self._get_products_data()
        page = self.paginate_queryset(data)

        if page is not None:
            serializer: Serializer = self.get_serializer(page, many=True)
            response: DRFResponse = self.get_paginated_response(
                serializer.data)

            return response

        serializer: Serializer = self.get_serializer(data, many=True)

        return Response({
            'products': serializer.data,
        })

    def _get_products_data(self) -> Any:
        filters: dict[str, Any] = self._get_filters_for_product()
        ordering: str = self.request.query_params.get('ordering', 'rating')

        return self.model.objects.get_product_list(filters, ordering)


class BaseProductItemView(RetrieveAPIView, BaseProductView):
    def get(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> DRFResponse:
        pk: Any = kwargs.get('pk')
        product: Any = self.model.objects.get_product_item(pk)
        serializer: Serializer = self.get_serializer(product)

        return Response({
            'product': serializer.data,
        })


class BaseAttributeView(FilterMixin, RetrieveAPIView, BaseProductView):
    def get(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> DRFResponse:
        category: str = self.request.query_params.get('category', '')[:-1]
        filters: dict[str, Any] = self._get_filters_for_attributes(category)
        data: Any = self.model.objects.get_attributes_count(filters, category)
        serializer: Serializer = self.get_serializer(data, many=True)

        return Response({
            'results': serializer.data,
        })
