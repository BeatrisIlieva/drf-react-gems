
from django.db import models

from djangoTSGems.products.models.references.color import Color
from djangoTSGems.products.models.references.stone import Stone


class StoneColor(models.Model):

    image = models.URLField()

    stone = models.ForeignKey(
        to=Stone,
        on_delete=models.CASCADE,
    )

    color = models.ForeignKey(
        to=Color,
        on_delete=models.CASCADE,
    )
