from django.db import models

from src.products.managers import ProductManager


class Product(models.Model):
    class Meta:
        abstract = True

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

    collection = models.ForeignKey(
        to='products.Collection',
        on_delete=models.CASCADE,
    )

    color = models.ForeignKey(
        to='products.Color',
        on_delete=models.CASCADE,
    )

    metal = models.ForeignKey(
        to='products.Metal',
        on_delete=models.CASCADE,
    )

    stone = models.ForeignKey(
        to='products.Stone',
        on_delete=models.CASCADE,
    )

    objects = ProductManager()

    def __str__(self):
        return f'{self.collection} {self.__class__.__name__}'
