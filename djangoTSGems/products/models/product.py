from django.db import models
from djangoTSGems.products.models.description import Description
from djangoTSGems.products.models.category import Category
from djangoTSGems.products.models.color import Color


class Product(models.Model):

    first_image_url = models.URLField()

    second_image_url = models.URLField()

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE
    )

    color = models.ForeignKey(
        to=Color,
        on_delete=models.CASCADE
    )

    description = models.ForeignKey(
        to=Description,
        on_delete=models.CASCADE,
    )
