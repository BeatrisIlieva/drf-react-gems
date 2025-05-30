from rest_framework import serializers

from src.products.serializers.base import BaseProductItemSerializer


def create_related_serializer(model_class):
    class RelatedSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = ['id', 'first_image']

    return RelatedSerializer


def create_product_item_serializer(model_class, inventory_model_class, inventory_serializer_base, many=True):
    related_serializer_cls = create_related_serializer(model_class)

    class InventorySerializer(inventory_serializer_base):
        class Meta(inventory_serializer_base.Meta):
            model = inventory_model_class

    class ProductSerializer(BaseProductItemSerializer):
        inventory = InventorySerializer(many=many, read_only=True)
        related_serializer_class = related_serializer_cls

        class Meta(BaseProductItemSerializer.Meta):
            model = model_class
            fields = BaseProductItemSerializer.base_fields

    return ProductSerializer
