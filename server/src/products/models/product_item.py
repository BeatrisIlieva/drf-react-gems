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

    stone_by_color = models.ManyToManyField(
        to='products.StoneByColor',
        through='products.ProductItemStoneByColor',
    )

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'


class ProductItemStoneByColor(models.Model):

    class Meta:
        unique_together = ('product', 'stone')
        verbose_name_plural = 'Stone by Color'

    product = models.ForeignKey(
        to='products.ProductItem',
        on_delete=models.CASCADE
    )

    stone = models.ForeignKey(
        to='products.StoneByColor',
        on_delete=models.CASCADE
    )
    

    def __str__(self):
        return f'{self.stone.color.name} {self.stone.stone.name}'
