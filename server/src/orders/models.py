from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model


import uuid

from src.orders.choices import OrderStatusChoices

UserModel = get_user_model()


class Order(models.Model):
    class Meta:
        ordering = ['-created_at']

    order_group = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    status = models.CharField(
        max_length=OrderStatusChoices.max_length(),
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
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

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
