from django.db import models

from src.products.managers import NeckwearManager
from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Neckwear(Product):
    objects = NeckwearManager()


class NeckwearSize(Size):
    pass


class NeckwearInventory(InventoryInfoMixin, Inventory):
    class Meta:
        unique_together = ('product', 'size')
        ordering = ['size__id']

    size = models.ForeignKey(
        to=NeckwearSize,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        to=Neckwear,
        on_delete=models.CASCADE,
        related_name='inventory',
    )
