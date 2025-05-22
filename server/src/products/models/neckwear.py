from django.db import models

from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Neckwear(Product):
    inventories = models.ManyToManyField(
        to='products.NeckwearInventory',
        through='products.NeckwearInventoryLink',
    )


class NeckwearSize(Size):
    pass


class NeckwearInventory(Inventory):
    size = models.ForeignKey(
        to=NeckwearSize,
        on_delete=models.CASCADE,
    )


class NeckwearInventoryLink(InventoryInfoMixin, models.Model):
    class Meta:
        unique_together = ('product', 'inventory')

    product = models.ForeignKey(
        to=Neckwear,
        on_delete=models.CASCADE
    )

    inventory = models.ForeignKey(
        to=NeckwearInventory,
        on_delete=models.CASCADE
    )
