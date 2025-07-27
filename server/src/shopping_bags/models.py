from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ShoppingBag(models.Model):
    class Meta:
        unique_together = [
            ('user', 'inventory'),
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

    inventory = models.ForeignKey(
        to='products.Inventory',
        on_delete=models.CASCADE,
        related_name='shopping_bag_items',
    )
