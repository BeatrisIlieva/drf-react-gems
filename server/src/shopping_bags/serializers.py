from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from typing import Any

from src.shopping_bags.models import ShoppingBag
from src.common.mixins import InventoryMixin


class ShoppingBagSerializer(serializers.ModelSerializer):
    content_type: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    product_info: serializers.SerializerMethodField = serializers.SerializerMethodField()
    total_price: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingBag
        fields = [
            'id',
            'user',
            'quantity',
            'created_at',
            'content_type',
            'object_id',
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

    def get_product_info(self, obj: Any) -> Any:
        return InventoryMixin.get_product_info(obj)

    def get_total_price(self, obj: Any) -> Any:
        return InventoryMixin.get_total_price_per_product(obj)
