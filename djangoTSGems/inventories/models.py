from django.db import models


class Inventory(models.Model):

    class Meta:
        unique_together = (
            'product',
            'size',
        )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    size = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
    )
