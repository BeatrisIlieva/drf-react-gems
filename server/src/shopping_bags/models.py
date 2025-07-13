# Shopping Bag Models
# This module contains the ShoppingBag model which represents items in a user's shopping cart.
# The model uses GenericForeignKey to support different types of inventory items (earwear, necklaces, etc.)

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ShoppingBag(models.Model):
    """
    ShoppingBag model represents items in a user's shopping cart.
    
    This model uses GenericForeignKey to support different types of inventory items
    (earwear, necklaces, rings, etc.) without needing separate models for each type.
    
    Key Features:
    - Supports both authenticated users and guest users (via guest_id)
    - Uses GenericForeignKey for flexible inventory item relationships
    - Enforces unique constraints to prevent duplicate items
    - Tracks quantity and creation timestamp
    """

    class Meta:
        # Unique constraints ensure that a user cannot have duplicate items in their bag
        # This prevents the same product from being added multiple times as separate entries
        unique_together = [
            # For authenticated users: user + content_type + object_id must be unique
            # This ensures one entry per product per user
            (
                'user',
                'content_type',
                'object_id'
            ),
            # For guest users: guest_id + content_type + object_id must be unique
            # This ensures one entry per product per guest session
            (
                'guest_id',
                'content_type',
                'object_id'
            ),
        ]
        # Order by creation date, newest first
        # This helps display recently added items at the top
        ordering = ['-created_at']

    # Quantity of the item in the shopping bag
    # PositiveIntegerField ensures only positive numbers and prevents negative quantities
    quantity = models.PositiveIntegerField()

    # Timestamp when the item was added to the shopping bag
    # auto_now_add=True automatically sets this when the record is created
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Foreign key to the user model for authenticated users
    # null=True and blank=True allow this to be empty for guest users
    # on_delete=CASCADE ensures that if a user is deleted, their shopping bag items are also deleted
    user = models.ForeignKey(
        to=UserModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    # UUID field for guest users who are not authenticated
    # null=True and blank=True allow this to be empty for authenticated users
    # db_index=True creates a database index for faster queries on guest_id
    # This allows the shopping bag to work for both logged-in and anonymous users
    guest_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )

    # Foreign key to ContentType model
    # ContentType is Django's way of tracking all models in the system
    # This tells us which type of model the object_id refers to
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    # The primary key of the specific inventory item
    # This works together with content_type to identify the exact product
    # PositiveIntegerField ensures only positive numbers
    object_id = models.PositiveIntegerField()

    # GenericForeignKey creates a flexible relationship to any model
    # 'content_type' and 'object_id' are the field names that store the relationship
    # This allows the shopping bag to contain different types of products (earwear, necklaces, etc.)
    # without needing separate models or fields for each product type
    inventory = GenericForeignKey(
        'content_type',
        'object_id',
    )
