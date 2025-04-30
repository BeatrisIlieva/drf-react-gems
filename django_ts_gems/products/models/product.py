from django.db import models

from django_ts_gems.products.models.relationships.category import Category
from django_ts_gems.products.models.relationships.collection import Collection
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.description import Description
from django_ts_gems.products.models.relationships.material import Material
from django_ts_gems.products.models.relationships.media import Media
from django_ts_gems.products.models.relationships.primary_stone import PrimaryStone
from django_ts_gems.products.models.relationships.reference import Reference
from django_ts_gems.products.models.relationships.stone import Stone


class Product(models.Model):
    
    # class Meta:
    #     ordering = ('?',)

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

    reference = models.ForeignKey(
        to=Reference,
        on_delete=models.CASCADE,
    )

    stones = models.ManyToManyField(
        to=Stone,
    )

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'
