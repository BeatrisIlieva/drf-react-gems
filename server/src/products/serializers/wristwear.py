from src.products.models.wristwear import Wristwear, WristwearInventory
from src.products.serializers.base import BaseProductItemSerializer
from src.products.serializers.inventory import SizedInventorySerializer
from src.products.serializers.utils import create_related_serializer


RelatedWristwearSerializer = create_related_serializer(Wristwear)


class WristwearInventorySerializer(SizedInventorySerializer):
    class Meta(SizedInventorySerializer.Meta):
        model = WristwearInventory


class WristwearSerializer(BaseProductItemSerializer):
    inventory = WristwearInventorySerializer(many=True, read_only=True)
    related_serializer_class = RelatedWristwearSerializer

    class Meta(BaseProductItemSerializer.Meta):
        model = Wristwear
        fields = BaseProductItemSerializer.base_fields
