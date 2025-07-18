from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

from src.products.models.inventory import Inventory

class ShoppingBag(models.Model):
    class Meta:
        unique_together = [
            # For authenticated users: user + inventory must be unique
            (
                'user',
                'inventory'
            ),
            # For guest users: guest_id + inventory must be unique
            (
                'guest_id',
                'inventory'
            ),
        ]
        ordering = ['-created_at']

    quantity = models.PositiveIntegerField()

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

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='shopping_bag_items',
    )
