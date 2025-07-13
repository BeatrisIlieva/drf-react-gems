"""
Review Model for DRF React Gems E-commerce Platform

This module defines the Review model which allows users to rate and comment
on products. The model uses Django's GenericForeignKey to work with any
product type (Earwear, Neckwear, etc.) without needing separate review
tables for each product category.

The Review model includes:
- Rating system (1-5 stars)
- Comment field for detailed feedback
- Approval system for moderation
- GenericForeignKey for flexible product relationships
- User association for tracking who wrote the review
"""

# Django imports for model functionality and user management
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Local imports for constants and validators
from src.products.constants import ReviewFieldLengths
from src.products.validators.comment import validate_comment_length

# Get the active user model (our custom UserCredential)
User = get_user_model()


class Review(models.Model):
    """
    Review model for user feedback on products.
    
    This model allows users to rate and comment on any product in the system.
    It uses Django's GenericForeignKey to work with different product types
    (Earwear, Neckwear, Fingerwear, Wristwear) without needing separate
    review tables for each category.
    
    The model includes an approval system where reviews must be approved
    before being displayed publicly, allowing for content moderation.
    
    Key features:
    - 1-5 star rating system
    - Text comments with length limits
    - Approval workflow for moderation
    - Generic relationship to any product type
    - User association for accountability
    """
    
    # Rating choices from 1 to 5 stars
    # This creates a dropdown in forms and admin
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    class Meta:
        # Order reviews by creation date (newest first)
        ordering = ['-created_at']
        
        # Ensure each user can only review each product once
        # This prevents spam and duplicate reviews
        unique_together = (
            'user',
            'content_type',
            'object_id'
        )
        
        # Custom permission for approving reviews
        # This allows admin to control who can approve reviews
        permissions = [
            (
                'approve_review',
                'Can approve reviews'
            ),
        ]

    # Rating field with choices from 1 to 5
    # This ensures only valid ratings are stored
    rating = models.IntegerField(
        choices=RATING_CHOICES,
    )

    # Comment field for detailed feedback
    # blank=False ensures comments are required
    # max_length prevents excessively long comments
    # validators=[validate_comment_length] enforces max_length at model level
    comment = models.TextField(
        max_length=ReviewFieldLengths.MAX_COMMENT_LENGTH,
        blank=False,
        validators=[validate_comment_length],
    )

    # Approval flag for content moderation
    # default=False means reviews start as unapproved
    # Only approved reviews are displayed publicly
    approved = models.BooleanField(
        default=False,
    )

    # Timestamp when the review was created
    # auto_now_add=True sets this automatically on creation
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # GenericForeignKey components for flexible product relationships
    # content_type stores which model the review is for (Earwear, Neckwear, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    # object_id stores the specific product's ID
    object_id = models.PositiveIntegerField()

    # GenericForeignKey combines content_type and object_id
    # This allows the review to be associated with any product type
    # The 'product' name makes it easy to access the related product
    product = GenericForeignKey(
        'content_type',
        'object_id',
    )

    # User who wrote the review
    # on_delete=models.CASCADE means if user is deleted, review is deleted
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """
        String representation of the review.
        
        Returns a descriptive string showing the product, user, and rating.
        This is used in Django admin and when converting objects to strings.
        """
        return f'{self.product} - {self.user.username} ({self.rating})'
