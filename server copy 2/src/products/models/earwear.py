from django.db import models

from src.products.managers import EarwearManager
from src.products.models.base import Inventory, Product


class Earwear(Product):
    objects = EarwearManager()


class EarwearInventory(Inventory):
    product = models.OneToOneField(
        to=Earwear,
        on_delete=models.CASCADE,
        related_name='inventory', 
    )
