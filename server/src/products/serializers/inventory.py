"""
This module contains the serializer for inventory items related to products.

It provides:
- Serialization of inventory fields such as size, quantity, and price
- Logic to expose content type and object ID for generic relations (so inventory can be linked to different product types)
- Used to serialize inventory data for product APIs
"""

from typing import Any
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from src.products.models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    content_type: serializers.SerializerMethodField = serializers.SerializerMethodField()
    object_id: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields: list[str] = [
            'id',
            'size',
            'quantity',
            'price',
            'content_type',
            'object_id'
        ]
        depth = 2

    def get_content_type(
        self,
        obj: Any
    ) -> str:
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.model

    def get_object_id(
        self,
        obj: Any
    ) -> Any:
        return obj.pk
