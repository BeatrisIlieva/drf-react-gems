from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MaxLengthValidator

from src.products.constants import ReviewFieldLengths

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

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    class Meta:
        ordering = ['-created_at']

        # Ensure each user can only review each product once
        unique_together = (
            'user',
            'content_type',
            'object_id',
        )

        # Custom permission for approving reviews
        # This allows admin to control who can approve reviews
        permissions = [
            (
                'approve_review',
                'Can approve reviews',
            ),
        ]

    rating = models.IntegerField(
        choices=RATING_CHOICES,
    )

    comment = models.TextField(
        validators=[
            MaxLengthValidator(
                ReviewFieldLengths.MAX_COMMENT_LENGTH,
            ),
        ],
    )

    # Only approved reviews are displayed publicly
    approved = models.BooleanField(
        default=False,
    )

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

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.product} - {self.user.username} ({self.rating})'
