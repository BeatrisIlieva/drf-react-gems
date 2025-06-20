from rest_framework import serializers


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection__name = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    is_sold_out = serializers.BooleanField()
    color__name = serializers.CharField()
    stone__name = serializers.CharField()
    metal__name = serializers.CharField()
    min = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    max = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    average_rating = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
