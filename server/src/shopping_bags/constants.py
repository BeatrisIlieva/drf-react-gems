# Shopping Bag Error Messages
# This module contains centralized error messages for the shopping bag functionality.
# Centralizing error messages makes them easier to maintain and ensures consistency
# across the application. It also makes it easier to internationalize these messages later.

class ShoppingBagErrorMessages:
    # Error message when a product cannot be found in the database
    # This typically occurs when trying to add a product that has been deleted
    # or when the object_id doesn't match any existing product
    PRODUCT_NOT_FOUND = 'Product not found'
    
    # Error message when trying to add more items than available in stock
    # The {quantity} placeholder is dynamically replaced with the actual available quantity
    # This helps users understand exactly how many items they can add
    INSUFFICIENT_STOCK = 'Only {quantity} items available in stock'
    
    # Error message when there's an issue calculating the total price
    # This could happen due to database issues, missing price data, or calculation errors
    ERROR_TOTAL_PRICE = 'Unable to calculate total price'
