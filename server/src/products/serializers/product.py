"""
This module contains concrete serializers for each product type and related attributes.

It provides:
- List and detail serializers for each product type (Earwear, Neckwear, Wristwear, Fingerwear)
- Attribute serializers for product properties like color, metal, stone, and collection
- All serializers are based on shared base serializers for consistency and reuse
- Used for product list/detail API endpoints and for serializing product attributes
"""

from typing import Type
from src.products.models.product import (
    Color,
    Earwear,
    Metal,
    Neckwear,
    Stone,
    Wristwear,
    Fingerwear,
    Collection
)
from src.products.serializers.base import (
    BaseAttributesSerializer,
    BaseProductItemSerializer,
    BaseProductListSerializer
)


class EarwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model: Type[Earwear] = Earwear


class NeckwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model: Type[Neckwear] = Neckwear


class WristwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model: Type[Wristwear] = Wristwear


class FingerwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model: Type[Fingerwear] = Fingerwear


class EarwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model: Type[Earwear] = Earwear


class NeckwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model: Type[Neckwear] = Neckwear


class WristwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model: Type[Wristwear] = Wristwear


class FingerwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model: Type[Fingerwear] = Fingerwear


class CollectionSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model: Type[Collection] = Collection


class ColorSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model: Type[Color] = Color


class MetalSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model: Type[Metal] = Metal


class StoneSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model: Type[Stone] = Stone
