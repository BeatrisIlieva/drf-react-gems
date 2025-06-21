from src.products.models.product import Earwear, Neckwear, Wristwear, Fingerwear
from src.products.serializers.base import BaseProductItemSerializer, BaseProductListSerializer


class EarwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Earwear


class NeckwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Neckwear


class WristwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Wristwear


class FingerwearListSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Fingerwear


class EarwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Earwear


class NeckwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Neckwear


class WristwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Wristwear


class FingerwearItemSerializer(BaseProductItemSerializer):
    class Meta(BaseProductItemSerializer.Meta):
        model = Fingerwear
