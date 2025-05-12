from django.db import models

from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Color(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin, models.Model):
    HEX_CODE_MAX_LENGTH = 7

    hex_code = models.CharField(
        max_length=HEX_CODE_MAX_LENGTH,
    )
