from typing import Type
from src.products.models.product import (
    Color,
    Metal,
    Stone,
    Collection
)
from src.products.serializers.product import (
    CollectionSerializer,
    ColorSerializer,
    EarwearItemSerializer,
    FingerwearItemSerializer,
    MetalSerializer,
    NeckwearItemSerializer,
    NeckwearListSerializer,
    EarwearListSerializer,
    StoneSerializer,
    WristwearItemSerializer,
    WristwearListSerializer,
    FingerwearListSerializer
)
from src.products.models import (
    Earwear,
    Neckwear,
    Wristwear,
    Fingerwear
)
from src.products.views.base import (
    BaseAttributeView,
    BaseProductItemView,
    BaseProductListView
)


class EarwearListView(BaseProductListView):
    model: Type[Earwear] = Earwear
    serializer_class = EarwearListSerializer


class NeckwearListView(BaseProductListView):
    model: Type[Neckwear] = Neckwear
    serializer_class = NeckwearListSerializer


class WristwearListView(BaseProductListView):
    model: Type[Wristwear] = Wristwear
    serializer_class = WristwearListSerializer


class FingerwearListView(BaseProductListView):
    model: Type[Fingerwear] = Fingerwear
    serializer_class = FingerwearListSerializer


class EarwearItemView(BaseProductItemView):
    model: Type[Earwear] = Earwear
    serializer_class = EarwearItemSerializer


class NeckwearItemView(BaseProductItemView):
    model: Type[Neckwear] = Neckwear
    serializer_class = NeckwearItemSerializer


class WristwearItemView(BaseProductItemView):
    model: Type[Wristwear] = Wristwear
    serializer_class = WristwearItemSerializer


class FingerwearItemView(BaseProductItemView):
    model: Type[Fingerwear] = Fingerwear
    serializer_class = FingerwearItemSerializer


class CollectionRetrieveView(BaseAttributeView):
    model: Type[Collection] = Collection
    serializer_class = CollectionSerializer


class ColorRetrieveView(BaseAttributeView):
    model: Type[Color] = Color
    serializer_class = ColorSerializer


class MetalRetrieveView(BaseAttributeView):
    model: Type[Metal] = Metal
    serializer_class = MetalSerializer


class StoneRetrieveView(BaseAttributeView):
    model: Type[Stone] = Stone
    serializer_class = StoneSerializer
