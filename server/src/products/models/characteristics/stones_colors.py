from django.db import models


class StoneColors(models.Model):

    image = models.URLField()

    color = models.ForeignKey(
        to='products.Color',
        on_delete=models.CASCADE,
    )

    stone = models.ForeignKey(
        to='products.Stone',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.color} {self.stone}'


class ProductItemStonesColors(models.Model):

    class Meta:
        unique_together = ('product_item', 'stones_colors')

    product_item = models.ForeignKey(
        to='products.ProductItem',
        on_delete=models.CASCADE
    )

    stones_colors = models.ForeignKey(
        to='products.StonesColors',
        on_delete=models.CASCADE
    )
