from rest_framework import serializers


def create_related_serializer(model_class):
    class RelatedSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = ['id', 'first_image']

    return RelatedSerializer
