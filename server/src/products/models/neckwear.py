from django.db import models

from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Neckwear(Product):
    pass


class NeckwearSize(Size):
    pass


class NeckwearInventory(InventoryInfoMixin, Inventory):
    class Meta:
        unique_together = ('product', 'size')

    size = models.ForeignKey(
        to=NeckwearSize,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        to=Neckwear,
        on_delete=models.CASCADE
    )
