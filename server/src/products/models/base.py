from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from src.products.models.inventory import Inventory
from src.products.models.review import Review


class BaseProduct(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    inventory = GenericRelation(Inventory)
    review = GenericRelation(Review)

    class Meta:
        abstract = True

    first_image = models.URLField(
        unique=True,
    )

    second_image = models.URLField(
        unique=True,
    )

    third_image = models.URLField(
        unique=True,
    )

    fourth_image = models.URLField(
        unique=True,
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

    target_gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.FEMALE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.collection} {self.__class__.__name__}'
