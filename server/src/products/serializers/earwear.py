from src.products.models.earwear import Earwear, EarwearInventory
from src.products.serializers.base import BaseProductItemSerializer
from src.products.serializers.inventory import SimpleInventorySerializer
from src.products.serializers.utils import create_related_serializer


RelatedEarwearSerializer = create_related_serializer(Earwear)


class EarwearInventorySerializer(SimpleInventorySerializer):
    class Meta(SimpleInventorySerializer.Meta):
        model = EarwearInventory


class EarwearSerializer(BaseProductItemSerializer):
    inventory = EarwearInventorySerializer(read_only=True)
    related_serializer_class = RelatedEarwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Earwear
        fields = BaseProductItemSerializer.base_fields
