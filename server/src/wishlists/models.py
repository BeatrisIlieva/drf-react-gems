# Wishlist Models
# This module contains the Wishlist model which manages user wishlist items.
# The model supports both authenticated users and guest users with proper constraints.

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Wishlist(models.Model):
    """
    Wishlist model for managing user wishlist items.
    
    This model allows users to save products to their wishlist for later reference.
    It supports both authenticated users and guest users, with proper constraints
    to prevent duplicate entries and ensure data integrity.
    
    Key Features:
    - GenericForeignKey relationship to any product type (earwear, necklaces, etc.)
    - Support for both authenticated users and guest users
    - Unique constraints to prevent duplicate items per user
    - Automatic timestamp tracking for item creation
    - Proper ordering by creation date (newest first)
    
    Relationships:
    - user: ForeignKey to UserModel (nullable for guest users)
    - guest_id: UUID field for guest user identification
    - content_type: ForeignKey to ContentType for generic relationships
    - object_id: PositiveIntegerField for the specific product ID
    - product: GenericForeignKey to the actual product object
    """
    
    class Meta:
        """
        Model metadata and constraints.
        
        unique_together constraints ensure that:
        1. Authenticated users cannot have duplicate items in their wishlist
        2. Guest users cannot have duplicate items in their wishlist
        3. Items are ordered by creation date (newest first)
        """
        unique_together = [
            # Prevents authenticated users from adding the same item twice
            (
                'user',
                'content_type',
                'object_id'
            ),
            # Prevents guest users from adding the same item twice
            (
                'guest_id',
                'content_type',
                'object_id'
            ),
        ]
        # Order items by creation date, newest first
        ordering = ['-created_at']

    # Timestamp when the item was added to the wishlist
    # Auto_now_add ensures this is set automatically on creation
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # ForeignKey to UserModel for authenticated users
    # Nullable and blank to support guest users
    # CASCADE ensures wishlist items are deleted when user is deleted
    user = models.ForeignKey(
        to=UserModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    # UUID field for guest user identification
    # Nullable and blank to support authenticated users
    # db_index=True for efficient querying of guest wishlists
    guest_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )

    # ForeignKey to ContentType for generic relationships
    # This allows the wishlist to work with any product type
    # CASCADE ensures wishlist items are deleted when content type is deleted
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    # PositiveIntegerField for the specific product ID
    # Must be positive to ensure valid object references
    object_id = models.PositiveIntegerField()

    # GenericForeignKey to the actual product object
    # This creates a generic relationship to any model
    # Uses content_type and object_id to resolve the actual object
    product = GenericForeignKey(
        'content_type',
        'object_id',
    )

    def __str__(self):
        """
        String representation of the wishlist item.
        
        Returns a human-readable string showing the user (or guest) and the product.
        This is useful for admin interface and debugging.
        
        Returns:
            str: String representation in format "user_email - product" or "Guest: guest_id - product"
        """
        user_info = self.user.email if self.user else f"Guest: {self.guest_id}"
        return f'{user_info} - {self.product}'
