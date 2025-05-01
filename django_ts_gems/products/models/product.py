from django.db import models


class Product(models.Model):
    first_image = models.URLField()

    second_image = models.URLField()

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
    )

    collection = models.ForeignKey(
        to='Collection',
        on_delete=models.CASCADE,
    )

    material = models.ForeignKey(
        to='Material',
        on_delete=models.CASCADE,
    )

    reference = models.ForeignKey(
        to='Reference',
        on_delete=models.CASCADE,
    )

    stones_colors = models.ManyToManyField(
        to='StonesColors',
    )

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'
