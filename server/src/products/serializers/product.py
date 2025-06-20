from rest_framework import serializers

from src.products.models.product import Earwear, Neckwear, Wristwear, Fingerwear


class BaseProductListSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    max_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    average_rating = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        fields = [
            'id',
            'first_image',
            'second_image',
            'collection__name',
            'is_sold_out',
            'color__name',
            'stone__name',
            'metal__name',
            'min_price',
            'max_price',
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
