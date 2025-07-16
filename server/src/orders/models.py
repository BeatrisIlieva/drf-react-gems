from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model

import uuid

from src.orders.choices import OrderStatusChoices

UserModel = get_user_model()


class Order(models.Model):
    """
    The Order model represents a single product order made by a user.
    It supports grouping multiple products into a single order (order_group),
    tracks order status, and uses GenericForeignKey to relate to any product type.
    """
    class Meta:
        ordering = ['-created_at']

    # order_group allows grouping multiple Order instances (products) into a single checkout event
    order_group = models.UUIDField(
        default=uuid.uuid4,  # Automatically generates a unique UUID for each group
        editable=False,      # Prevents manual editing in admin or forms
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

    # content_type and object_id together enable a GenericForeignKey
    # This allows the Order to reference any product type (Earwear, Neckwear, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    # Stores the primary key of the related product
    object_id = models.PositiveIntegerField()

    # inventory is a GenericForeignKey, combining content_type and object_id
    # This enables the Order to relate to any product instance, regardless of its model
    # Benefits: avoids the need for separate order tables for each product type
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
