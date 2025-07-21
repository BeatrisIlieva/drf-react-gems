from django.db import models
from django.contrib.auth import get_user_model
import uuid
from src.orders.choices import OrderStatusChoices

UserModel = get_user_model()


class Order(models.Model):
    """
    The Order model represents a single product order made by a user.

    Key Features:
    - Each order is linked to a specific inventory item (size/variation) via a ForeignKey.
    - Supports grouping multiple products into a single order event using order_group (UUID).
    - Tracks order status (pending, completed, etc.).
    - Stores the quantity and creation timestamp for each order item.
    - Linked to the user who placed the order.

    Relationships:
    - inventory: ForeignKey to Inventory, which in turn is linked to the actual product (Earwear, Neckwear, etc.).
    - user: ForeignKey to the user who placed the order.
    - order_group: UUID to group multiple order items from a single checkout.
    """
    class Meta:
        ordering = ['-created_at']

    order_group = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Groups multiple order items from a single checkout event."
    )

    status = models.CharField(
        max_length=OrderStatusChoices.max_length(),
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
        help_text="Current status of the order (e.g., pending, completed)."
    )

    quantity = models.PositiveIntegerField(
        help_text="Number of units of the inventory item ordered."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the order was created."
    )

    inventory = models.ForeignKey(
        to='products.Inventory',
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="The inventory item (size/variation) being ordered."
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        help_text="The user who placed the order."
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
