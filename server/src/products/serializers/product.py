"""
This module contains concrete serializers for each product type and related attributes.

It provides:
- List and detail serializers for each product type (Earring, Necklace, Pendant, Bracelet, Watch)
- Attribute serializers for product properties like color, metal, stone, and collection
- All serializers are based on shared base serializers for consistency and reuse
- Used for product list/detail API endpoints and for serializing product attributes
"""

from src.products.models.product import (
    Bracelet,
    Color,
    DropEarring,
    Metal,
    Necklace,
    Pendant,
    Ring,
    Stone,
    Collection,
    StudEarring,
    Watch,
)

from src.products.serializers.base import (
    BaseAttributesSerializer,
    BaseProductItemSerializer,
    BaseProductListSerializer,
)


class StudEarringListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = StudEarring


class DropEarringListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = DropEarring


class NecklaceListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Necklace


class PendantListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Pendant


class BraceletListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Bracelet


class RingListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Ring


class WatchListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Watch


class StudEarringItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = StudEarring


class BraceletItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Bracelet


class WatchItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Watch


class RingItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Ring


class DropEarringItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = DropEarring


class NecklaceItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Necklace


class PendantItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Pendant


class CollectionSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Collection


class ColorSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Color


class MetalSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Metal


class StoneSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Stone
