from django.contrib.contenttypes.models import ContentType


class InventoryMixin:
    """
    Mixin class that provides utility methods for working with inventory objects.

    This mixin is designed to work with any object that has an 'inventory' attribute
    (like shopping bag items and order items). It provides methods
    to extract standardized product information and calculate prices.

    The mixin uses ContentType to dynamically determine the product type.
    """

    @staticmethod
    def get_product_info(obj):
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
            'product_id': product.id,  # Unique product identifier
            # Product collection name
            'collection': str(product.collection),
            # Product price as float
            'price': float(inventory.price),
            'first_image': product.first_image,  # First product image
            'available_quantity': inventory.quantity,  # Available stock
            # Product size (if any)
            'size': str(getattr(inventory, 'size', '')),
            'metal': str(product.metal.name),  # Metal type
            'stone': str(product.stone.name),  # Stone type
            'color': str(product.color.name),  # Color
            'category': model_name,  # Product category
        }

    @staticmethod
    def get_total_price_per_product(obj):
        try:
            # Calculate total price by multiplying unit price by quantity
            # round() ensures we get exactly 2 decimal places for currency
            return round(obj.inventory.price * obj.quantity, 2)

        except Exception:
            # Return 0.0 if calculation fails (e.g., missing attributes)
            # This prevents the application from crashing due to data issues
            return 0.0
