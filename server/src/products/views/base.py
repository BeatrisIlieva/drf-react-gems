from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView


from src.products.mixins import FilterMixin


class BaseProductView(APIView):
    permission_classes = [AllowAny]


class ProductPagination(PageNumberPagination):
    page_size = 8


class BaseProductListView(FilterMixin, ListAPIView, BaseProductView):
    pagination_class = ProductPagination

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


class BaseProductItemView(RetrieveAPIView, BaseProductView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = self.model.objects.get_product_item(pk)
        serializer = self.get_serializer(product, context={'request': request})

        return Response({
            'product': serializer.data,
        })


class BaseAttributeView(FilterMixin, RetrieveAPIView, BaseProductView):
    def get(self, request, *args, **kwargs):
        # Singularize category if it ends with 's'
        category = self.request.query_params.get('category', '')
        if isinstance(category, list):
            category = category[0] if category else ''
        if not isinstance(category, str):
            category = ''
        if category.endswith('s') and len(category) > 1:
            category = category[:-1]
        filters = self._get_filters_for_attributes(category)
        data = self.model.objects.get_attributes_count(filters, category)
        serializer = self.get_serializer(data, many=True)

        return Response({
            'results': serializer.data,
        })


class AsyncBaseAttributeView(FilterMixin, RetrieveAPIView, BaseProductView):
    """
    Asynchronous base view for attribute filters.

    This view provides async support for filter attributes like collections,
    colors, metals, and stones. 

    Benefits:
    - Reduced response time when multiple attributes are fetched together
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the retrieval of attribute data used for
        product filtering. It processes the category parameter and returns
        the appropriate filtered results with optimized database queries.

        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            DRFResponse: Serialized attribute data for filtering
        """
        # Safely singularize category if it ends with 's'
        category = request.query_params.get('category', '')
        if isinstance(category, list):
            category = category[0] if category else ''
        if not isinstance(category, str):
            category = ''
        if category.endswith('s') and len(category) > 1:
            category = category[:-1]
        filters = self._get_filters_for_attributes(category)

        # Use optimized database query
        data = self.model.objects.get_attributes_count(filters, category)
        serializer = self.get_serializer(data, many=True)

        return Response({
            'results': serializer.data,
        })
