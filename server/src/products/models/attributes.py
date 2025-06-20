from src.products.models.mixins import NameFieldMixin
from src.products.managers.attributes import (
    CollectionManager,
    ColorManager,
    MetalManager,
    StoneManager
)


class Collection(NameFieldMixin):
    objects = CollectionManager()


class Color(NameFieldMixin):
    objects = ColorManager()


class Metal(NameFieldMixin):
    objects = MetalManager()


class Stone(NameFieldMixin):
    objects = StoneManager()
