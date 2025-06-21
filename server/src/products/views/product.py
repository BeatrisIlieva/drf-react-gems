from src.products.serializers.product import EarwearItemSerializer, FingerwearItemSerializer, NeckwearItemSerializer, NeckwearListSerializer, EarwearListSerializer, WristwearItemSerializer, WristwearListSerializer, FingerwearListSerializer
from src.products.models import Earwear, Neckwear, Wristwear, Fingerwear
from src.products.views.base import BaseProductItemView, BaseProductListView


class EarwearListView(BaseProductListView):
    model = Earwear
    serializer_class = EarwearListSerializer


class NeckwearListView(BaseProductListView):
    model = Neckwear
    serializer_class = NeckwearListSerializer


class WristwearListView(BaseProductListView):
    model = Wristwear
    serializer_class = WristwearListSerializer


class FingerwearListView(BaseProductListView):
    model = Fingerwear
    serializer_class = FingerwearListSerializer


class EarwearItemView(BaseProductItemView):
    model = Earwear
    serializer_class = EarwearItemSerializer


class NeckwearItemView(BaseProductItemView):
    model = Neckwear
    serializer_class = NeckwearItemSerializer


class WristwearItemView(BaseProductItemView):
    model = Wristwear
    serializer_class = WristwearItemSerializer


class FingerwearItemView(BaseProductItemView):
    model = Fingerwear
    serializer_class = FingerwearItemSerializer
