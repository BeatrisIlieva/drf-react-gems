from django.db import models

from src.products.managers import StoneManager
from src.products.models.mixins import NameFieldMixin


class Collection(NameFieldMixin):
    pass


class Color(NameFieldMixin, models.Model):
    HEX_CODE_MAX_LENGTH = 7

    hex_code = models.CharField(
        max_length=HEX_CODE_MAX_LENGTH,
    )


class Metal(NameFieldMixin):
    pass


class Stone(NameFieldMixin, models.Model):
    image = models.URLField()
    objects = StoneManager()
