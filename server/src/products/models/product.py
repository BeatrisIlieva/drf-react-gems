from src.products.models.base import BaseProduct
from src.products.managers import EarwearManager, NeckwearManager, WristwearManager, FingerwearManager
from src.products.managers.product import CollectionManager, ColorManager, MetalManager, StoneManager
from src.products.mixins import NameFieldMixin


class Earwear(BaseProduct):
    objects = EarwearManager()


class Neckwear(BaseProduct):
    objects = NeckwearManager()


class Fingerwear(BaseProduct):
    objects = FingerwearManager()


class Wristwear(BaseProduct):
    objects = WristwearManager()


class Collection(NameFieldMixin):
    objects = CollectionManager()


class Color(NameFieldMixin):
    objects = ColorManager()


class Metal(NameFieldMixin):
    objects = MetalManager()


class Stone(NameFieldMixin):
    objects = StoneManager()
