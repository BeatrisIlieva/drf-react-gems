"""
Inventory Model for DRF React Gems E-commerce Platform

This module defines the Inventory model which tracks stock levels and pricing
for products. The model uses Django's GenericForeignKey to work with any
product type (Earwear, Neckwear, etc.) and includes size variations.

The Inventory model includes:
- Quantity tracking for stock management
- Price field with decimal precision for currency
- Size relationship for product variations
- GenericForeignKey for flexible product relationships
- Size model for standardized size options
"""

# Django imports for model functionality and validation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

# Local imports for constants and mixins
from src.products.constants import InventoryFiledLengths
from src.products.mixins import NameFieldMixin


class Inventory(models.Model):
    """
    Inventory model for tracking product stock and pricing.
    
    This model manages the inventory levels and pricing for all products
    in the system. It uses Django's GenericForeignKey to work with different
    product types (Earwear, Neckwear, Fingerwear, Wristwear) without needing
    separate inventory tables for each category.
    
    The model supports size variations, allowing the same product to have
    different stock levels and prices for different sizes (e.g., Small, Medium, Large).
    
    Key features:
    - Quantity tracking for stock management
    - Price field with decimal precision for accurate pricing
    - Size relationship for product variations
    - Generic relationship to any product type
    - Validation to prevent negative quantities and prices
    """
    
    class Meta:
        # Order inventory records by ID for consistent ordering
        ordering = ['id']

    # Quantity field for stock tracking
    # PositiveIntegerField ensures only positive numbers
    # This prevents negative stock levels
    quantity = models.PositiveIntegerField()

    # Price field with decimal precision for currency
    # max_digits and decimal_places ensure accurate pricing
    # MinValueValidator prevents negative prices
    price = models.DecimalField(
        max_digits=InventoryFiledLengths.PRICE_MAX_DIGITS,
        decimal_places=InventoryFiledLengths.PRICE_DECIMAL_PLACES,
        validators=[
            MinValueValidator(0)  # Ensures price is not negative
        ]
    )

    # Size relationship for product variations
    # This allows the same product to have different sizes
    # on_delete=models.CASCADE means if size is deleted, inventory is deleted
    size = models.ForeignKey(
        to='products.Size',
        on_delete=models.CASCADE,
    )

    # GenericForeignKey components for flexible product relationships
    # content_type stores which model the inventory is for (Earwear, Neckwear, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    # object_id stores the specific product's ID
    object_id = models.PositiveIntegerField()

    # GenericForeignKey combines content_type and object_id
    # This allows the inventory to be associated with any product type
    # The 'product' name makes it easy to access the related product
    product = GenericForeignKey(
        'content_type',
        'object_id'
    )

    def __str__(self):
        """
        String representation of the inventory record.
        
        Returns a descriptive string showing quantity, price, and size.
        This is used in Django admin and when converting objects to strings.
        """
        return f'Quantity: {self.quantity} / Price: {self.price} / Size: {self.size.name}'


class Size(NameFieldMixin):
    """
    Size model for product size variations.
    
    This model inherits from NameFieldMixin to get a standardized name field.
    It's used to define size options for products (e.g., Small, Medium, Large).
    
    The model is simple but essential for inventory management, allowing
    the same product to have different stock levels and prices for different sizes.
    """
    pass
