from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from src.products.managers import ProductManager
from src.products.models.inventory import Inventory
from src.products.models.review import Review


class BaseProduct(models.Model):
    inventory = GenericRelation(Inventory)
    review = GenericRelation(Review)

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


class Earwear(BaseProduct):
    pass


class Neckwear(BaseProduct):
    pass


class Fingerwear(BaseProduct):
    pass


class Wristwear(BaseProduct):
    pass
