from django.db import models


class ProductVariant(models.Model):
    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACES = 2

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )

    quantity = models.PositiveIntegerField()

    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )
    
    product_item = models.ForeignKey(
        to='products.ProductItem',
        on_delete=models.CASCADE,
    )
