from django.db import models
from djangoTSGems.products.models.description import Description
from djangoTSGems.products.models.category import Category
from djangoTSGems.products.models.gemstone import Gemstone


class Product(models.Model):

    first_image_url = models.URLField()

    second_image_url = models.URLField()

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE
    )

    description = models.ForeignKey(
        to=Description,
        on_delete=models.CASCADE,
    )

    gemstone = models.ForeignKey(
        to=Gemstone,
        on_delete=models.CASCADE
    )
