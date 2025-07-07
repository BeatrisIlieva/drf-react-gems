from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from src.wishlists.models import Wishlist
from src.products.serializers.base import ProductListDataMixin


class WishlistSerializer(serializers.ModelSerializer, ProductListDataMixin):
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
        """
        Returns product data in the same format as product list views
        """
        product_obj = obj.product
        
        # If the wishlist item is an inventory item, get the actual product
        if hasattr(product_obj, 'product') and hasattr(product_obj, 'size'):
            # This is an inventory item, get the actual product
            actual_product = product_obj.product
            product_data = self.get_product_list_data(actual_product)
            
            # Add inventory-specific data
            if product_data:
                product_data['size'] = product_obj.size.name
                product_data['price'] = product_obj.price
                product_data['available_quantity'] = product_obj.quantity
                
            return product_data
        else:
            # This is a direct product
            return self.get_product_list_data(product_obj)