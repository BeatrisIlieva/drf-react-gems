"""
Product Managers for DRF React Gems E-commerce Platform

This module contains specific manager classes for each product type and attribute.
These managers inherit from the base managers to provide specialized functionality
for different product categories while maintaining consistent query patterns.

The managers include:
- Product managers: EarwearManager, NeckwearManager, WristwearManager, FingerwearManager
- Attribute managers: ColorManager, CollectionManager, MetalManager, StoneManager
"""

# Type hints for better code documentation and IDE support
from typing import Type, Any
from src.products.managers.base import BaseAttributesManager, BaseProductManager


class EarwearManager(BaseProductManager[Type[Any]]):
    """
    Manager for Earwear products.
    
    This manager inherits from BaseProductManager to provide optimized
    query methods specifically for earwear products. It uses the same
    query patterns as other product managers but works with the Earwear model.
    
    The manager provides methods for retrieving earwear products with
    proper annotations, filtering, and ordering capabilities.
    """
    pass


class NeckwearManager(BaseProductManager[Type[Any]]):
    """
    Manager for Neckwear products.
    
    This manager inherits from BaseProductManager to provide optimized
    query methods specifically for neckwear products. It uses the same
    query patterns as other product managers but works with the Neckwear model.
    
    The manager provides methods for retrieving neckwear products with
    proper annotations, filtering, and ordering capabilities.
    """
    pass


class WristwearManager(BaseProductManager[Type[Any]]):
    """
    Manager for Wristwear products.
    
    This manager inherits from BaseProductManager to provide optimized
    query methods specifically for wristwear products. It uses the same
    query patterns as other product managers but works with the Wristwear model.
    
    The manager provides methods for retrieving wristwear products with
    proper annotations, filtering, and ordering capabilities.
    """
    pass


class FingerwearManager(BaseProductManager[Type[Any]]):
    """
    Manager for Fingerwear products.
    
    This manager inherits from BaseProductManager to provide optimized
    query methods specifically for fingerwear products. It uses the same
    query patterns as other product managers but works with the Fingerwear model.
    
    The manager provides methods for retrieving fingerwear products with
    proper annotations, filtering, and ordering capabilities.
    """
    pass


class ColorManager(BaseAttributesManager[Type[Any]]):
    """
    Manager for Color attributes.
    
    This manager inherits from BaseAttributesManager to provide optimized
    query methods for color attributes. It includes functionality for
    counting how many products use each color, which is useful for
    building filter options in the frontend.
    
    The manager provides methods for retrieving colors with product counts
    and filtering capabilities.
    """
    pass


class CollectionManager(BaseAttributesManager[Type[Any]]):
    """
    Manager for Collection attributes.
    
    This manager inherits from BaseAttributesManager to provide optimized
    query methods for collection attributes. It includes functionality for
    counting how many products belong to each collection, which is useful
    for building filter options and collection pages in the frontend.
    
    The manager provides methods for retrieving collections with product counts
    and filtering capabilities.
    """
    pass


class MetalManager(BaseAttributesManager[Type[Any]]):
    """
    Manager for Metal attributes.
    
    This manager inherits from BaseAttributesManager to provide optimized
    query methods for metal attributes. It includes functionality for
    counting how many products use each metal type, which is useful for
    building filter options in the frontend.
    
    The manager provides methods for retrieving metals with product counts
    and filtering capabilities.
    """
    pass


class StoneManager(BaseAttributesManager[Type[Any]]):
    """
    Manager for Stone attributes.
    
    This manager inherits from BaseAttributesManager to provide optimized
    query methods for stone attributes. It includes functionality for
    counting how many products use each stone type, which is useful for
    building filter options in the frontend.
    
    The manager provides methods for retrieving stones with product counts
    and filtering capabilities.
    """
    pass
