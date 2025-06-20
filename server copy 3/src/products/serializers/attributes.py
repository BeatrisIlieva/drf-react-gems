from rest_framework import serializers

from src.products.models.attributes import Stone


class BaseAttributesSerializer(serializers.ModelSerializer):
    pass


class StoneSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
    count = serializers.IntegerField()
