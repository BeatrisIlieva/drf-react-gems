from src.products.models.base import BaseProduct

from src.products.managers.product import (
    BraceletManager,
    CollectionManager,
    ColorManager,
    EarringManager,
    MetalManager,
    NecklaceManager,
    PendantManager,
    RingManager,
    StoneManager,
    WatchManager,
)
from src.products.mixins import NameFieldMixin



class Earring(BaseProduct):
    objects = EarringManager()


class Necklace(BaseProduct):
    objects = NecklaceManager()


class Pendant(BaseProduct):
    objects = PendantManager()


class Ring(BaseProduct):
    objects = RingManager()


class Bracelet(BaseProduct):
    objects = BraceletManager()


class Watch(BaseProduct):
    objects = WatchManager()


class Collection(NameFieldMixin):
    objects = CollectionManager()


class Color(NameFieldMixin):
    objects = ColorManager()


class Metal(NameFieldMixin):
    objects = MetalManager()


class Stone(NameFieldMixin):
    objects = StoneManager()
