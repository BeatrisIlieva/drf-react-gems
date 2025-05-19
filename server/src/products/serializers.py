from rest_framework import serializers

from src.products.models.relationships.category import Category


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection__name = serializers.CharField()
    category__name = serializers.CharField()
    reference__name = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    stones = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_null=True, allow_blank=True)
        )
    )
    min_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    materials_count = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    is_sold_out = serializers.BooleanField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
