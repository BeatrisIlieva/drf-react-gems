from src.products.models.base import BaseProduct
from src.products.managers import EarwearManager, NeckwearManager, WristwearManager, FingerwearManager


class Earwear(BaseProduct):
    objects = EarwearManager()


class Neckwear(BaseProduct):
    objects = NeckwearManager()


class Fingerwear(BaseProduct):
    objects = FingerwearManager()


class Wristwear(BaseProduct):
    objects = WristwearManager()
