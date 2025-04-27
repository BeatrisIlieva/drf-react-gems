from django.db import models

from django_ts_gems.products.models.references.category import Category
from django_ts_gems.products.models.references.collection import Collection
from django_ts_gems.products.models.references.color import Color
from django_ts_gems.products.models.references.description import Description
from django_ts_gems.products.models.references.material import Material
from django_ts_gems.products.models.references.media import Media
from django_ts_gems.products.models.references.primary_stone import PrimaryStone
from django_ts_gems.products.models.references.stone import Stone


class Product(models.Model):
    class Meta:
        unique_together = ('category', 'collection', 'primary_stone')

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

    media = models.ForeignKey(
        to=Media,
        on_delete=models.CASCADE,
    )

    primary_stone = models.ForeignKey(
        to=PrimaryStone,
        on_delete=models.CASCADE,
    )

    colors = models.ManyToManyField(
        to=Color,
    )

    materials = models.ManyToManyField(
        to=Material,
    )

    stones = models.ManyToManyField(
        to=Stone,
    )
