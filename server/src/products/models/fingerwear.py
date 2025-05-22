from django.db import models

from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Fingerwear(Product):
    inventories = models.ManyToManyField(
        to='products.FingerwearInventory',
        through='products.FingerwearInventoryLink',
    )


class FingerwearSize(Size):
    pass


class FingerwearInventory(Inventory):
    size = models.ForeignKey(
        to=FingerwearSize,
        on_delete=models.CASCADE,
    )


class FingerwearInventoryLink(InventoryInfoMixin, models.Model):
    class Meta:
        unique_together = ('product', 'inventory')

    product = models.ForeignKey(
        to=Fingerwear,
        on_delete=models.CASCADE,
    )

    inventory = models.ForeignKey(
        to=FingerwearInventory,
        on_delete=models.CASCADE,
    )
