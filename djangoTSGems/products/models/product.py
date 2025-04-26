from django.db import models

from djangoTSGems.products.models.references.category import Category
from djangoTSGems.products.models.references.collection import Collection
from djangoTSGems.products.models.references.description import Description
from djangoTSGems.products.models.references.material import Material
from djangoTSGems.products.models.references.media import Media
from djangoTSGems.products.models.references.stone_color import StoneColor


class Product(models.Model):
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
    )

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
    )

    description = models.ForeignKey(
        to=Description,
        on_delete=models.CASCADE,
    )

    material = models.ManyToManyField(
        to=Material,
    )

    media = models.ForeignKey(
        to=Media,
        on_delete=models.CASCADE,
    )

    stone_color = models.ManyToManyField(
        to=StoneColor,
    )
