from django.db import models

from django_ts_gems.products.choices import ColorChoices


class Color(models.Model):
    HEX_CODE_MAX_LENGTH = 7

    name = models.CharField(
        max_length=ColorChoices.max_length(),
        choices=ColorChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This color already exists.'
        }
    )

    hex_code = models.CharField(
        max_length=HEX_CODE_MAX_LENGTH,
    )
