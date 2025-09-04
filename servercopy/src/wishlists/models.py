from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Wishlist(models.Model):
    class Meta:
        unique_together = [
            # Prevents authenticated users from adding the same item twice
            ('user', 'content_type', 'object_id'),
        ]

        ordering = ['-created_at']

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    # ForeignKey to ContentType for generic relationships
    # This allows the wishlist to work with any product type
    # CASCADE ensures wishlist items are deleted when content type is deleted
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    # GenericForeignKey to the actual product object
    # This creates a generic relationship to any model
    # Uses content_type and object_id to resolve the actual object
    product = GenericForeignKey(
        'content_type',
        'object_id',
    )

    def __str__(self):
        user_info = self.user.email
        return f'{user_info} - {self.product}'
