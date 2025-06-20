from src.products.managers import CollectionManager, ColorManager, MetalManager, StoneManager
from src.products.models.mixins import NameFieldMixin


class Collection(NameFieldMixin):
    objects = CollectionManager()


class Color(NameFieldMixin):
    objects = ColorManager()


class Metal(NameFieldMixin):
    objects = MetalManager()


class Stone(NameFieldMixin):
    objects = StoneManager()
