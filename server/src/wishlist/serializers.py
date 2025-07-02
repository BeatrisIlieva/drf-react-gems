from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from src.wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'guest_id',
            'created_at',
            'content_type',
            'object_id',
            'product_info',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'guest_id',
            'product_info',
        ]
        
    def get_product_info(self, obj):
        if obj.product:
            return {
                'id': obj.product.id,
                'first_image': obj.product.first_image,
                'second_image': obj.product.second_image,
                'collection': obj.product.collection.name,
                'color': obj.product.color.name,
                'metal': obj.product.metal.name,
                'stone': obj.product.stone.name,
                'product_type': obj.content_type.model,
            }
        return None