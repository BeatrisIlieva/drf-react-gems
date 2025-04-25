from django.db import models


from djangoTSGems.products.choices import BraceletTypeChoices
from djangoTSGems.products.mixins import ChoicesMaxLengthMixin
from djangoTSGems.products.models.description import Description
from djangoTSGems.products.models.label import Label
from djangoTSGems.products.models.material import Material
from djangoTSGems.products.models.media import Media
from djangoTSGems.products.models.size import Size
from djangoTSGems.products.models.stone_color import StoneColor


class Product(models.Model):
    class Meta:
        abstract = True

    media = models.ForeignKey(
        to=Media,
        on_delete=models.CASCADE,
    )

    label = models.ForeignKey(
        to=Label,
        on_delete=models.CASCADE,
    )

    description = models.ForeignKey(
        to=Description,
        on_delete=models.CASCADE,
    )

    material = models.ManyToManyField(
        to=Material,
    )

    stone_color = models.ManyToManyField(
        to=StoneColor,
    )


class Bracelet(Product):
    pass

class Earring(Product):
    pass


class Necklace(Product):
    pass


class Ring(Product):
    pass
