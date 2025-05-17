from django.db import models


class Product(models.Model):
    class Meta:
        unique_together = ('category', 'collection', 'reference', 'first_image', 'size')

    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACES = 2

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    first_image = models.ForeignKey(
        to='products.FirstImage',
        on_delete=models.CASCADE,
    )

    second_image = models.ForeignKey(
        to='products.SecondImage',
        on_delete=models.CASCADE,
    )

    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )

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
    )

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'
