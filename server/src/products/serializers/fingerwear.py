
from src.products.models.fingerwear import Fingerwear, FingerwearInventory
from src.products.serializers.base import BaseProductItemSerializer
from src.products.serializers.inventory import SizedInventorySerializer
from src.products.serializers.utils import create_related_serializer


RelatedFingerwearSerializer = create_related_serializer(Fingerwear)


class FingerwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = FingerwearInventory


class FingerwearSerializer(BaseProductItemSerializer):
    inventory = FingerwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedFingerwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Fingerwear
        fields = BaseProductItemSerializer.base_fields
