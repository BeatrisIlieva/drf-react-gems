from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class SizedInventorySerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'size', 'quantity', 'content_type', 'object_id']
        depth = 2

    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.id

    def get_object_id(self, obj):
        return obj.pk


class SimpleInventorySerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'quantity', 'content_type', 'object_id']
        depth = 2

    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.id

    def get_object_id(self, obj):
        return obj.pk
