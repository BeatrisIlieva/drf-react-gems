from rest_framework import serializers


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    collection__name = serializers.CharField()

    reference__name = serializers.CharField()

    first_image = serializers.CharField()

    second_image = serializers.CharField()

    price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    total_quantity = serializers.IntegerField()

    is_sold_out = serializers.BooleanField()

    materials_count = serializers.IntegerField()

    stones = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_null=True, allow_blank=True)
        )
    )
