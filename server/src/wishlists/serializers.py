from typing import Any, Dict
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from rest_framework import serializers

from src.wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    content_type: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    product_info: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields: list[str] = [
            'id',
            'user',
            'guest_id',
            'created_at',
            'content_type',
            'object_id',
            'product_info',
        ]
        read_only_fields: list[str] = [
            'id',
            'created_at',
            'user',
            'guest_id',
            'product_info',
        ]

    def get_product_info(
        self,
        obj: Any
    ) -> Dict[str, Any]:
        product = obj.product

        avg_rating = product.review.filter(
            approved=True
        ).aggregate(
            avg=Avg('rating')
        )['avg'] or 0

        inventory_items = product.inventory.all()
        if inventory_items:
            prices = [item.price for item in inventory_items]
            min_price = min(prices)
            max_price = max(prices)
        else:
            min_price = max_price = 0

        is_sold_out = not inventory_items.filter(
            quantity__gt=0
        ).exists()

        return {
            'id': product.id,
            'first_image': product.first_image,
            'second_image': product.second_image,
            'collection__name': product.collection.name,
            'color__name': product.color.name,
            'stone__name': product.stone.name,
            'metal__name': product.metal.name,
            'is_sold_out': is_sold_out,
            'average_rating': round(avg_rating, 2),
            'min_price': min_price,
            'max_price': max_price,
        }
