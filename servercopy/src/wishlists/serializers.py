from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from rest_framework import serializers

from src.wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    """
    This serializer handles the conversion of Wishlist model instances to JSON
    and includes additional computed fields for product information and ratings.

    Key Features:
    - Includes product information from the related product
    - Calculates average rating from approved reviews
    - Provides price range (min/max) from inventory items
    - Determines if product is sold out based on inventory
    - Handles GenericForeignKey relationships
    - Provides read-only fields for computed values
    """

    # SlugRelatedField for content_type allows us to use the model name as a string
    # instead of the numeric ID.
    # The 'model' field returns the model name (e.g., 'earwear', 'necklace')
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
    )

    # SerializerMethodField for product_info allows us to include additional
    # information about the product without modifying the model
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        # Fields to include in the serialized output
        fields = [
            'id',
            'user',
            'created_at',
            'content_type',
            'object_id',
            'product_info',
        ]
        # Fields that cannot be modified through the API
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'product_info',
        ]

    def get_product_info(self, obj):
        """
        This method retrieves detailed information about the product including:
        - Basic product details (id, images, collection, color, stone, metal)
        - Average rating from approved reviews
        - Price range from inventory items
        - Sold out status based on inventory availability
        """
        # Get the related product object through GenericForeignKey
        product = obj.product

        # Calculate average rating from approved reviews only
        # Uses Django's aggregation to get the average rating
        # Returns 0 if no approved reviews exist
        avg_rating = (
            product.review.filter(
                approved=True,
            ).aggregate(
                avg=Avg(
                    'rating',
                )
            )['avg']
            or 0
        )

        # Get all inventory items for the product
        inventory_items = product.inventory.all()
        if inventory_items:
            # Calculate price range from all inventory items
            prices = [item.price for item in inventory_items]
            min_price = min(prices)
            max_price = max(prices)
        else:
            # No inventory items available
            min_price = max_price = 0

        # Determine if product is sold out
        # Checks if any inventory items have quantity > 0
        is_sold_out = not inventory_items.filter(
            quantity__gt=0,
        ).exists()

        # Return comprehensive product information
        return {
            'id': product.id,
            'first_image': product.first_image,
            'second_image': product.second_image,
            'collection__name': product.collection.name,
            'color__name': product.color.name,
            'stone__name': product.stone.name,
            'metal__name': product.metal.name,
            'is_sold_out': is_sold_out,
            # Round to 2 decimal places
            'average_rating': round(avg_rating, 2),
            'min_price': min_price,
            'max_price': max_price,
        }
