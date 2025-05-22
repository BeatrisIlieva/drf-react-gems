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

    objects = ProductManager()

    def __str__(self):
        return f'{self.collection} {self.reference}'


class Inventory(models.Model):
    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACES = 2

    class Meta:
        abstract = True

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Price: {self.price} - Quantity: {self.quantity}'


class Size(models.Model):
    class Meta:
        abstract = True

    SIZE_MAX_DIGITS = 5
    SIZE_DECIMAL_PLACES = 2

    name = models.DecimalField(
        max_digits=SIZE_MAX_DIGITS,
        decimal_places=SIZE_DECIMAL_PLACES,
    )

    def __str__(self):
        return f'Size: {self.name}'
