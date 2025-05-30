from rest_framework import serializers


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection__name = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    is_sold_out = serializers.BooleanField()
    min = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    max = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
