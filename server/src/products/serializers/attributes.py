from rest_framework import serializers

from src.products.models.attributes import Collection, Color, Metal, Stone


class BaseAttributesSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        fields = ['id', 'name', 'count']


class CollectionSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Collection


class ColorSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Color


class MetalSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Metal


class StoneSerializer(BaseAttributesSerializer):
    class Meta(BaseAttributesSerializer.Meta):
        model = Stone
