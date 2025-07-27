"""
This module contains specific manager classes for each product type and attribute.
These managers inherit from the base managers to provide specialized functionality
for different product categories while maintaining consistent query patterns.
"""

from src.products.managers.base import (
    BaseAttributesManager,
    BaseProductManager,
)


class EarwearManager(BaseProductManager):
    pass


class NeckwearManager(BaseProductManager):
    pass


class WristwearManager(BaseProductManager):
    pass


class FingerwearManager(BaseProductManager):
    pass


class ColorManager(BaseAttributesManager):
    pass


class CollectionManager(BaseAttributesManager):
    pass


class MetalManager(BaseAttributesManager):
    pass


class StoneManager(BaseAttributesManager):
    pass
