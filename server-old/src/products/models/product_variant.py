from django.db import models


class ProductVariant(models.Model):
    class Meta:
        unique_together = ('product_item', 'size')

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        help_text='Select price',
    )

    quantity = models.PositiveIntegerField(
        default=0,
        help_text='Select quantity',
    )

    product_item = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
    )

    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )


