# models.py for the Orders app
# This file defines the Order model, which represents a single product order in the e-commerce system.
# The model uses advanced Django features like GenericForeignKey to allow flexible product relations.
# Every line is documented for beginners to understand the purpose and reasoning behind each implementation.

from django.contrib.contenttypes.models import ContentType  # Used for generic relations to any model
from django.contrib.contenttypes.fields import GenericForeignKey  # Enables linking to any model instance
from django.db import models  # Django's ORM base for model definitions
from django.contrib.auth import get_user_model  # To reference the custom user model

import uuid  # For generating unique order group IDs

from src.orders.choices import OrderStatusChoices  # Custom choices for order status (Pending, Completed, etc.)

# Get the active user model (custom user model for authentication)
UserModel = get_user_model()


class Order(models.Model):
    """
    The Order model represents a single product order made by a user.
    It supports grouping multiple products into a single order (order_group),
    tracks order status, and uses GenericForeignKey to relate to any product type.
    """
    class Meta:
        # Orders are sorted by creation date, newest first, for easy retrieval in UIs
        ordering = ['-created_at']

    # order_group allows grouping multiple Order instances (products) into a single checkout event
    # This is useful for multi-product orders, tracking them as a single transaction
    order_group = models.UUIDField(
        default=uuid.uuid4,  # Automatically generates a unique UUID for each group
        editable=False,      # Prevents manual editing in admin or forms
    )

    # status tracks the current state of the order (Pending, Completed, etc.)
    # Uses a custom choices class for maintainability and to avoid magic strings
    status = models.CharField(
        max_length=OrderStatusChoices.max_length(),  # Ensures DB field is large enough for all choices
        choices=OrderStatusChoices.choices,          # Restricts values to defined statuses
        default=OrderStatusChoices.PENDING           # New orders start as Pending
    )

    # quantity stores how many units of the product were ordered
    # PositiveIntegerField ensures only valid (non-negative) quantities
    quantity = models.PositiveIntegerField()

    # created_at records when the order was placed
    # auto_now_add automatically sets this field on creation
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # content_type and object_id together enable a GenericForeignKey
    # This allows the Order to reference any product type (Earwear, Neckwear, etc.)
    content_type = models.ForeignKey(
        ContentType,            # Points to the model (table) of the product
        on_delete=models.CASCADE,  # If the product type is deleted, the order is deleted
    )

    object_id = models.PositiveIntegerField()  # Stores the primary key of the related product

    # inventory is a GenericForeignKey, combining content_type and object_id
    # This enables the Order to relate to any product instance, regardless of its model
    # Benefits: avoids the need for separate order tables for each product type
    inventory = GenericForeignKey(
        'content_type',  # Name of the content_type field
        'object_id',     # Name of the object_id field
    )

    # user is a ForeignKey to the user who placed the order
    # on_delete=models.CASCADE ensures orders are deleted if the user is deleted
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        # Returns a human-readable string for the order, useful in admin and debugging
        return f"Order {self.id} by {self.user.username}"
