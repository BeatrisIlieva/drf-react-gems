from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from src.shopping_bags.models import ShoppingBag


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
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'product_info',
            'total_price_per_product'
        ]
        depth = 3

    def get_product_info(self, obj):
        inventory = obj.inventory
        if not inventory:
            return {}

        product = getattr(inventory, 'product', None)
        if not product:
            return {}

        product_content_type = ContentType.objects.get_for_model(
            product.__class__
        )
        model_name = product_content_type.model.capitalize()

        return {
            'product_id': product.id,
            'collection': str(product.collection),
            'price': float(inventory.price),
            'first_image': product.first_image,
            'available_quantity': inventory.quantity,
            'size': str(getattr(inventory, 'size', '')),
            'metal': str(product.metal.name),
            'stone': str(product.stone.name),
            'color': str(product.color.name),
            'category': model_name,
        }

    def get_total_price_per_product(self, obj):
        try:
            return round(obj.inventory.price * obj.quantity, 2)
        except Exception:
            return 0
