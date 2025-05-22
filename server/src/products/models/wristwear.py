from django.db import models

from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Wristwear(Product):
    inventories = models.ManyToManyField(
        to='products.WristwearInventory',
        through='products.WristwearInventoryLink',
    )


class WristwearSize(Size):
    pass


class WristwearInventory(Inventory):
    size = models.ForeignKey(
        to=WristwearSize,
        on_delete=models.CASCADE,
    )


class WristwearInventoryLink(InventoryInfoMixin, models.Model):
    class Meta:
        unique_together = ('product', 'inventory')

    product = models.ForeignKey(
        to=Wristwear,
        on_delete=models.CASCADE
    )

    inventory = models.ForeignKey(
        to=WristwearInventory,
        on_delete=models.CASCADE
    )