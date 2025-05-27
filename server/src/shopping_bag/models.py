from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ShoppingBag(models.Model):
    QUANTITY_MIN_VALUE = 1

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    inventory = GenericForeignKey(
        'content_type',
        'object_id',
    )
