# Wishlist Constants
# This module contains error message constants used throughout the wishlist functionality.
# These constants provide standardized error messages for consistent user experience.

class WishlistErrorMessages:
    """
    Error message constants for wishlist functionality.
    
    This class contains standardized error messages used throughout the wishlist
    application to provide consistent user feedback and error handling.
    
    These messages are used by services, views, and serializers to ensure
    uniform error reporting across the wishlist feature.
    """
    
    # Error message when a requested product cannot be found in the database
    # Used when users try to add products that don't exist or have been removed
    PRODUCT_NOT_FOUND = 'Product not found'
    
    # Error message when a user tries to add an item that's already in their wishlist
    # Prevents duplicate entries and provides clear feedback to users
    ITEM_ALREADY_EXISTS = 'Item already in wishlist'
    
    # Error message when a wishlist item cannot be found for deletion or modification
    # Used when users try to remove items that don't exist or have already been removed
    ITEM_NOT_FOUND = 'Wishlist item not found'
    
    # Error message for invalid content type or object ID combinations
    # Used when the generic foreign key relationship is malformed or invalid
    ERROR_INVALID_CONTENT_TYPE_OR_ID = 'Invalid content type or object ID'
