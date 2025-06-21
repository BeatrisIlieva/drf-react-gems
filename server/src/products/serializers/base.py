from django.db.models import Avg
from rest_framework import serializers


from src.products.serializers.inventory import InventorySerializer
from src.products.serializers.review import ReviewSerializer


class BaseProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    is_sold_out = serializers.BooleanField()
    collection__name = serializers.CharField()
    color__name = serializers.CharField()
    stone__name = serializers.CharField()
    metal__name = serializers.CharField()
    min_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    max_price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    class Meta:
        fields = [
            'id',
            'first_image',
            'second_image',
            'collection__name',
            'color__name',
            'stone__name',
            'metal__name',
            'is_sold_out',
            'average_rating',
            'min_price',
            'max_price'
        ]
        depth = 2


class AverageRatingField(serializers.Field):
    def to_representation(self, value):
        avg = value.review.aggregate(avg=Avg('rating'))['avg'] or 0
        return round(avg, 2)


class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'first_image']
        model = None


class BaseProductItemSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)
    average_rating = AverageRatingField(source='*')
    related_collection_products = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        depth = 2

    def get_related_collection_products(self, obj):
        model_class = obj.__class__

        related_products = model_class.objects.filter(
            collection=obj.collection
        )

        class DynamicRelatedProductSerializer(RelatedProductSerializer):
            class Meta(RelatedProductSerializer.Meta):
                model = model_class

        serializer = DynamicRelatedProductSerializer(
            related_products, many=True)

        return serializer.data
