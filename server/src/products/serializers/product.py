from rest_framework import serializers

from src.products.models.product import Earwear, Neckwear, Wristwear, Fingerwear


class BaseProductListSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    max_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    average_rating = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    is_sold_out = serializers.BooleanField()
    collection__name = serializers.CharField()
    color__name = serializers.CharField()
    stone__name = serializers.CharField()
    metal__name = serializers.CharField()

    class Meta:
        fields = [
            'id',
            'first_image',
            'second_image',
            'collection__name',
            'color__name',
            'stone__name',
            'metal__name',
            'min_price',
            'max_price',
            'is_sold_out',
            'average_rating',
        ]
        depth = 2


class EarwearSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Earwear


class NeckwearSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Neckwear


class WristwearSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Wristwear


class FingerwearSerializer(BaseProductListSerializer):
    class Meta(BaseProductListSerializer.Meta):
        model = Fingerwear
