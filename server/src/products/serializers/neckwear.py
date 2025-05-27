from src.products.models.neckwear import Neckwear, NeckwearInventory
from src.products.serializers.base import BaseProductItemSerializer
from src.products.serializers.inventory import SizedInventorySerializer
from src.products.serializers.utils import create_related_serializer


RelatedNeckwearSerializer = create_related_serializer(Neckwear)


class NeckwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = NeckwearInventory


class NeckwearSerializer(BaseProductItemSerializer):
    inventory = NeckwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedNeckwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Neckwear
        fields = BaseProductItemSerializer.base_fields
