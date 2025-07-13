"""
Common Mixins for DRF React Gems E-commerce Platform

This module contains reusable mixin classes that provide common functionality
across different parts of the application. Mixins are a way to share code
between classes without using inheritance.

The InventoryMixin provides utility methods for working with product inventory
data, including extracting product information and calculating prices.
"""

# Type hints for better code documentation and IDE support
from typing import Any, Dict
# ContentType is used to get information about Django models dynamically
from django.contrib.contenttypes.models import ContentType


class InventoryMixin:
    """
    Mixin class that provides utility methods for working with inventory objects.
    
    This mixin is designed to work with any object that has an 'inventory' attribute
    (like shopping bag items, wishlist items, order items). It provides methods
    to extract standardized product information and calculate prices.
    
    The mixin uses ContentType to dynamically determine the product type,
    making it flexible for different product categories (earwear, neckwear, etc.).
    """
    
    @staticmethod
    def get_product_info(obj: Any) -> Dict[str, Any]:
        """
        Extract standardized product information from an inventory object.
        
        This method takes any object with an 'inventory' attribute and returns
        a dictionary with consistent product information. It's used across
        different parts of the application (shopping bags, wishlists, orders)
        to provide uniform product data.
        
        Args:
            obj: Any object that has an 'inventory' attribute (shopping bag item,
                 wishlist item, order item, etc.)
        
        Returns:
            Dict containing standardized product information including:
            - product_id: Unique identifier for the product
            - collection: Product collection name
            - price: Product price as float
            - first_image: URL or path to the first product image
            - available_quantity: Number of items available in inventory
            - size: Product size (if applicable)
            - metal: Metal type used in the jewelry
            - stone: Stone type used in the jewelry
            - color: Color of the product
            - category: Product category (Earwear, Neckwear, etc.)
        
        Example:
            If obj is a shopping bag item, this method will return product info
            that can be displayed in the shopping cart or order summary.
        """
        # Get the inventory object from the passed object
        inventory = obj.inventory
        if not inventory:
            return {}

        # Get the product from the inventory
        # This uses getattr for safety in case the attribute doesn't exist
        product = getattr(inventory, 'product', None)
        if not product:
            return {}

        # Use ContentType to dynamically get the model information
        # ContentType is a Django utility that stores information about models
        # This allows us to get the model name without hardcoding it
        product_content_type = ContentType.objects.get_for_model(
            product.__class__
        )
        # Capitalize the model name for display purposes
        model_name = product_content_type.model.capitalize()

        # Return a standardized dictionary with product information
        # This ensures consistent data structure across the application
        return {
            'product_id': product.id,                    # Unique product identifier
            'collection': str(product.collection),       # Product collection name
            'price': float(inventory.price),            # Product price as float
            'first_image': product.first_image,         # First product image
            'available_quantity': inventory.quantity,    # Available stock
            'size': str(getattr(inventory, 'size', '')), # Product size (if any)
            'metal': str(product.metal.name),           # Metal type
            'stone': str(product.stone.name),           # Stone type
            'color': str(product.color.name),           # Color
            'category': model_name,                     # Product category
        }

    @staticmethod
    def get_total_price_per_product(obj: Any) -> float:
        """
        Calculate the total price for a product based on quantity and unit price.
        
        This method multiplies the inventory price by the quantity to get
        the total cost for that specific product. It's used in shopping bags,
        orders, and other places where we need to calculate line item totals.
        
        Args:
            obj: Any object that has 'inventory' and 'quantity' attributes
                 (shopping bag item, order item, etc.)
        
        Returns:
            float: The total price for the product (price * quantity)
                  Returns 0.0 if calculation fails
        
        Example:
            If a shopping bag item has quantity=2 and inventory.price=100.00,
            this method returns 200.00
        """
        try:
            # Calculate total price by multiplying unit price by quantity
            # round() ensures we get exactly 2 decimal places for currency
            return round(obj.inventory.price * obj.quantity, 2)
        except Exception:
            # Return 0.0 if calculation fails (e.g., missing attributes)
            # This prevents the application from crashing due to data issues
            return 0.0
