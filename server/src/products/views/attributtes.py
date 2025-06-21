from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.products.mixins import FilterMixin
from src.products.models.attributes import Collection, Color, Metal, Stone
from src.products.serializers.attributes import CollectionSerializer, ColorSerializer, MetalSerializer, StoneSerializer


class BaseAttributeView(FilterMixin, RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        category = self.request.query_params.get('category')[:-1]
        filters = self._get_filters_for_attributes(category)
        data = self.model.objects.get_attributes_count(filters, category)

        serializer = self.get_serializer(data, many=True)

        return Response({
            'results': serializer.data,
        })


class CollectionRetrieveView(BaseAttributeView):
    model = Collection
    serializer_class = CollectionSerializer


class ColorRetrieveView(BaseAttributeView):
    model = Color
    serializer_class = ColorSerializer


class MetalRetrieveView(BaseAttributeView):
    model = Metal
    serializer_class = MetalSerializer


class StoneRetrieveView(BaseAttributeView):
    model = Stone
    serializer_class = StoneSerializer
