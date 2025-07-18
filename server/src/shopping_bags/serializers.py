from rest_framework import serializers

from src.shopping_bags.models import ShoppingBag
from src.common.mixins import InventoryMixin


class ShoppingBagSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShoppingBag model.

    This serializer handles the conversion of ShoppingBag model instances to JSON
    and includes additional computed fields for product information and total price.

    Key Features:
    - Includes product information from the related inventory item
    - Calculates total price for each item
    - Provides read-only fields for computed values
    """

    inventory = serializers.PrimaryKeyRelatedField(queryset=ShoppingBag._meta.get_field('inventory').related_model.objects.all())
    product_info = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingBag
        fields = [
            'id',
            'user',
            'quantity',
            'created_at',
            'inventory',
            'product_info',
            'total_price',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'product_info',
            'total_price'
        ]
        depth = 3

    def get_product_info(self, obj):
        return InventoryMixin.get_product_info(obj)

    def get_total_price(self, obj):
        return InventoryMixin.get_total_price_per_product(obj)
