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
            'product_info',
        ]
        
    def get_product_info(self, obj):
        """Get product information using the generic foreign key"""
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


class WishlistCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = Wishlist
        fields = [
            'content_type',
            'object_id',
        ]
        
    def validate(self, attrs):
        """Validate that the product exists"""
        content_type = attrs['content_type']
        object_id = attrs['object_id']
        
        # Check if the product exists
        model_class = content_type.model_class()
        if not model_class.objects.filter(id=object_id).exists():
            raise serializers.ValidationError("Product does not exist.")
            
        return attrs


class WishlistDeleteSerializer(serializers.Serializer):
    """Serializer for wishlist delete operation (used for documentation)"""
    content_type = serializers.CharField(
        help_text="Product type (earwear, neckwear, fingerwear, wristwear)"
    )
    object_id = serializers.IntegerField(
        help_text="Product ID"
    )