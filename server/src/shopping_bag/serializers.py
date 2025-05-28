from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from src.shopping_bag.models import ShoppingBag


class ShoppingBagSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    product_info = serializers.SerializerMethodField()
    total_price_per_product = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingBag
        fields = [
            'id',
            'user',
            'quantity',
            'created_at',
            'content_type',
            'object_id',
            'product_info',
            'total_price_per_product',
        ]
        read_only_fields = ['id', 'created_at',
                            'user', 'product_info', 'total_price_per_product']

    def get_product_info(self, obj):
        inventory = obj.inventory
        if not inventory:
            return {}

        product = getattr(inventory, 'product', None)
        if not product:
            return {}

        return {
            'product_id': product.id,
            'collection': str(product.collection),
            'reference': str(product.reference),
            'price': float(product.price),
            'first_image': product.first_image,
            'available_quantity': inventory.quantity,
            'size': str(getattr(inventory, 'size', '')),
        }

    def get_total_price_per_product(self, obj):
        try:
            return round(obj.inventory.product.price * obj.quantity, 2)
        except Exception:
            return 0
        
