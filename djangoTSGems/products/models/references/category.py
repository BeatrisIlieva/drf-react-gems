
from django.db import models

from djangoTSGems.products.choices import CategoryChoices


class Category(models.Model):

    category = models.CharField(
        max_length=CategoryChoices.max_length(),
        choices=CategoryChoices.choices,
    )
