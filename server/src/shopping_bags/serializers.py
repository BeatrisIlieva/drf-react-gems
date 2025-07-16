from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from typing import Any

from src.shopping_bags.models import ShoppingBag
from src.common.mixins import InventoryMixin


class ShoppingBagSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShoppingBag model.
    
    This serializer handles the conversion of ShoppingBag model instances to JSON
    and includes additional computed fields for product information and total price.
    
    Key Features:
    - Includes product information from the related inventory item
    - Calculates total price for each item
    - Handles GenericForeignKey relationships
    - Provides read-only fields for computed values
    """
    
    # SlugRelatedField for content_type allows us to use the model name as a string
    # instead of the numeric ID.
    # The 'model' field returns the model name (e.g., 'earwear', 'necklace')
    content_type: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    
    # SerializerMethodField for product_info allows us to include additional
    # information about the product without modifying the model
    # This field is computed dynamically based on the inventory relationship
    product_info: serializers.SerializerMethodField = serializers.SerializerMethodField()
    
    # SerializerMethodField for total_price calculates the total cost for this item
    # (price * quantity) without storing it in the database
    total_price: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingBag
        # Fields to include in the serialized output
        # These fields will be included in API responses
        fields = [
            'id',
            'user',
            'quantity',
            'created_at',
            'content_type',
            'object_id',
            'product_info',
            'total_price',
        ]
        # Fields that cannot be modified through the API
        # These are computed or automatically set fields
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'product_info',
            'total_price'
        ]
        # Depth of 3 means nested serialization will go 3 levels deep
        # This is useful for including related object data in the response
        depth = 3

    def get_product_info(self, obj: Any) -> Any:
        """
        Get product information for the shopping bag item.
        
        This method uses the InventoryMixin to retrieve standardized product information
        regardless of the specific product type (earwear, necklace, etc.).
        """
        return InventoryMixin.get_product_info(obj)

    def get_total_price(self, obj: Any) -> Any:
        """
        Calculate the total price for this shopping bag item.
        
        This method calculates the total cost by multiplying the item's price
        by the quantity in the shopping bag.
        """
        return InventoryMixin.get_total_price_per_product(obj)
