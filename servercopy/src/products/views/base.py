from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status

from src.products.mixins import FilterMixin
from src.products.utils import get_valid_categories


class ProductPagination(PageNumberPagination):
    page_size = 8


class BaseProductListView(FilterMixin, ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def list(self, request, *args, **kwargs):
        data = self._get_products_data()
        page = self.paginate_queryset(data)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            return response

        serializer = self.get_serializer(data, many=True)

        return Response(
            {
                'products': serializer.data,
            }
        )

    def _get_products_data(self):
        filters = self._get_filters_for_product()
        ordering = self.request.query_params.get('ordering', 'rating')

        return self.model.objects.get_product_list(filters, ordering)


class BaseProductItemView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = self.model.objects.get_product_item(pk)
        serializer = self.get_serializer(
            product,
            context={'request': request},
        )

        return Response(
            {
                'product': serializer.data,
            }
        )


class BaseAttributeView(FilterMixin, RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            category = self.request.query_params.get('category', '')

            if not isinstance(category, str):
                category = ''

            if category.endswith('s') and len(category) > 1:
                category = category[:-1]

            valid_categories = get_valid_categories()

            if category and category not in valid_categories:
                return Response(
                    {'error': 'Invalid category'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            filters = self._get_filters_for_attributes(category)
            data = self.model.objects.get_attributes_count(filters, category)
            serializer = self.get_serializer(data, many=True)

            return Response({'results': serializer.data})

        except Exception as e:

            return Response(
                {'error': 'Resource not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
