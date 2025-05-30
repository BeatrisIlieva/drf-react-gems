from src.products.models.base import Product
from django.contrib.contenttypes.fields import GenericRelation
from src.products.models import Inventory


class Earwear(Product):
    inventory = GenericRelation(Inventory)


class Neckwear(Product):
    inventory = GenericRelation(Inventory)


class Fingerwear(Product):
    inventory = GenericRelation(Inventory)


class Wristwear(Product):
    inventory = GenericRelation(Inventory)
