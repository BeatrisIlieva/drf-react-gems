from django.db import models

from djangoTSGems.products.models.category import Category
from djangoTSGems.products.models.collection import Collection
from djangoTSGems.products.models.description import Description
from djangoTSGems.products.models.design import Design
from djangoTSGems.products.models.material import Material
from djangoTSGems.products.models.stone_color import StoneColor


class Product(models.Model):

    image = models.URLField()

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE
    )

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE
    )

    description = models.ForeignKey(
        to=Description,
        on_delete=models.CASCADE,
    )

    design = models.ForeignKey(
        to=Design,
        on_delete=models.CASCADE,
    )

    material = models.ForeignKey(
        to=Material,
        on_delete=models.CASCADE,
    )

    stone_color = models.ForeignKey(
        to=StoneColor,
        on_delete=models.CASCADE,
    )
