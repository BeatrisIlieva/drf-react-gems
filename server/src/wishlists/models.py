from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Wishlist(models.Model):
    class Meta:
        unique_together = [
            (
                'user',
                'content_type',
                'object_id'
            ),
            (
                'guest_id',
                'content_type',
                'object_id'
            ),
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

    guest_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    product = GenericForeignKey(
        'content_type',
        'object_id',
    )

    def __str__(self):
        user_info = self.user.email if self.user else f"Guest: {self.guest_id}"
        return f'{user_info} - {self.product}'
