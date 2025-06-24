from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.core.validators import MinValueValidator
from django.db import models

from src.products.mixins import NameFieldMixin


class Inventory(models.Model):
    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACES = 2

    class Meta:
        ordering = ['id']

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        validators=[
            MinValueValidator(0)
        ]
    )

    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()

    product = GenericForeignKey(
        'content_type',
        'object_id'
    )

    def __str__(self):
        return f'Quantity: {self.quantity} / Price: {self.price} / Size: {self.size.name}'


class Size(NameFieldMixin):
    pass
