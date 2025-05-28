from django.db import models

from src.products.managers import WristwearManager
from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Wristwear(Product):
    objects = WristwearManager()


class WristwearSize(Size):
    pass


class WristwearInventory(InventoryInfoMixin, Inventory):
    class Meta:
        unique_together = ('product', 'size')
        ordering = ['size__id']

    size = models.ForeignKey(
        to=WristwearSize,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        to=Wristwear,
        on_delete=models.CASCADE,
        related_name='inventory',
    )
