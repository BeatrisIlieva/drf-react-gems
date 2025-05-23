from django.db import models

from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Fingerwear(Product):
    pass


class FingerwearSize(Size):
    pass


class FingerwearInventory(InventoryInfoMixin, Inventory):
    class Meta:
        unique_together = ('product', 'size')

    size = models.ForeignKey(
        to=FingerwearSize,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        to=Fingerwear,
        on_delete=models.CASCADE,
    )
