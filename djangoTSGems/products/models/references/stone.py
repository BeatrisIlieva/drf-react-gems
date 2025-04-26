from django.db import models

from djangoTSGems.products.choices import StoneChoices
from djangoTSGems.products.models.references.color import Color


class Stone(models.Model):

    stone = models.CharField(
        max_length=StoneChoices.max_length(),
        choices=StoneChoices.choices,
    )

    image = models.URLField()

    colors = models.ManyToManyField(
        to=Color,
        through='StoneColor',
    )

    def __str__(self):
        return self.get_stone_display()
