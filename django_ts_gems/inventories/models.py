from django.db import models


class Inventory(models.Model):
    class Meta:
        unique_together = ('product', 'size')
        verbose_name_plural = 'Inventories'

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
    )

    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )
