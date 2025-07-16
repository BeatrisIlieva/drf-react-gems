"""
This module contains specific manager classes for each product type and attribute.
These managers inherit from the base managers to provide specialized functionality
for different product categories while maintaining consistent query patterns.
"""


from typing import Type, Any
from src.products.managers.base import BaseAttributesManager, BaseProductManager


class EarwearManager(BaseProductManager[Type[Any]]):
    pass


class NeckwearManager(BaseProductManager[Type[Any]]):
    pass


class WristwearManager(BaseProductManager[Type[Any]]):
    pass


class FingerwearManager(BaseProductManager[Type[Any]]):
    pass


class ColorManager(BaseAttributesManager[Type[Any]]):
    pass


class CollectionManager(BaseAttributesManager[Type[Any]]):
    pass


class MetalManager(BaseAttributesManager[Type[Any]]):
    pass


class StoneManager(BaseAttributesManager[Type[Any]]):
    pass
