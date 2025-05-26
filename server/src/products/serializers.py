from rest_framework import serializers


from src.products.models.earwear import Earwear
from src.products.models.fingerwear import Fingerwear, FingerwearInventory
from src.products.models.review import Review


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection__name = serializers.CharField()
    reference__name = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    total_quantity = serializers.IntegerField()
    is_sold_out = serializers.BooleanField()
    materials_count = serializers.IntegerField()
    stones = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_null=True, allow_blank=True)
        )
    )


class EarwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earwear
        fields = '__all__'
        depth = 2


class RelatedFingerwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerwear
        fields = ['id', 'first_image']


class FingerwearInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FingerwearInventory
        fields = ['size', 'quantity']
        depth = 2


class FingerwearSerializer(serializers.ModelSerializer):
    inventory = FingerwearInventorySerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Fingerwear
        fields = [
            'id',
            'first_image',
            'second_image',
            'price',
            'created_at',
            'collection',
            'material',
            'reference',
            'stone_by_color',
            'inventory',
            'related_products',
        ]
        depth = 3

    def get_related_products(self, obj):
        related = Fingerwear.objects.filter(
            collection=obj.collection,
            reference=obj.reference
        )

        return RelatedFingerwearSerializer(related, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment',
                  'created_at', 'content_type', 'object_id']
        read_only_fields = ['user', 'created_at']
