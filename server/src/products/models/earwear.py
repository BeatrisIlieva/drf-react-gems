from django.db import models

from src.products.models.base import Inventory, Product


class Earwear(Product):
    pass


class EarwearInventory(Inventory):
    product = models.OneToOneField(
        to=Earwear,
        on_delete=models.CASCADE,
    )
