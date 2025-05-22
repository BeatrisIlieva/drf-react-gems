from django.db import models

from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Size(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin):
    pass


class ProductSize(models.Model):
    class Meta:
        unique_together = ('product', 'size')

    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACES = 2

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        'products.Size',
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} - {self.size} | Price: {self.price} | Qty: {self.quantity}"
