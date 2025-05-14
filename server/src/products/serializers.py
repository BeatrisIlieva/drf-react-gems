from rest_framework import serializers

from src.products.models.product import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1
