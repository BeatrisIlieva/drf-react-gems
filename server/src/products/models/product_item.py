from django.db import models

from src.products.managers import ProductManager


class ProductItem(models.Model):

    first_image = models.URLField(
        unique=True,
        error_messages={
            'unique': 'This image already exists.'
        }
    )

    second_image = models.URLField(
        unique=True,
        error_messages={
            'unique': 'This image already exists.'
        }
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

    objects = ProductManager()

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'
