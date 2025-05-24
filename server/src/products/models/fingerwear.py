from django.db import models

from src.products.managers import FingerwearManager
from src.products.mixins import InventoryInfoMixin
from src.products.models.base import Inventory, Product, Size


class Fingerwear(Product):
    objects = FingerwearManager()


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
        related_name='fingerwearinventory'
    )
