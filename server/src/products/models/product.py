from django.db import models

from src.products.managers import ProductManager


class Product(models.Model):

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

    created_at = models.DateTimeField(
        auto_now_add=True,
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

    stone_by_color = models.ForeignKey(
        to='products.StoneByColor',
        on_delete=models.CASCADE,
    )

    sizes = models.ManyToManyField(
        to='products.Size',
        through='products.ProductSize'
    )

    objects = ProductManager()

    def __str__(self):
        return f'{self.collection} {self.reference} {self.category}'

