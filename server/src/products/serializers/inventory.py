from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from src.products.models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            'id',
            'size',
            'quantity',
            'price',
            'content_type',
            'object_id'
        ]
        depth = 2

    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.model

    def get_object_id(self, obj):
        return obj.pk
