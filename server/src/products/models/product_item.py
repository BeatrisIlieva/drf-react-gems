from django.db import models


class ProductItem(models.Model):
    first_image = models.URLField()

    second_image = models.URLField()

    category = models.ForeignKey(
        to='products.Category',
        on_delete=models.CASCADE,
    )

    collection = models.ForeignKey(
        to='products.Collection',
        on_delete=models.CASCADE,
    )

    material = models.ForeignKey(
        to='products.Material',
        on_delete=models.CASCADE,
    )

    reference = models.ForeignKey(
        to='products.Reference',
        on_delete=models.CASCADE,
    )

    stones_colors = models.ManyToManyField(
        to='products.StonesColors',
        through='products.ProductItemStonesColors',
    )

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'


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
