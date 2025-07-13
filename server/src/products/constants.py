"""
Product Constants for DRF React Gems E-commerce Platform

This module contains constants used throughout the products app to ensure
consistency in field lengths, validation rules, and error messages.
These constants help maintain data integrity and provide clear error
feedback to users.

The constants are organized by functionality:
- ReviewFieldLengths: Field length constraints for review data
- InventoryFiledLengths: Field constraints for inventory pricing
- ReviewErrorMessages: User-friendly error messages for review operations
- NameFieldLengths: Standard name field length for various entities
"""


class ReviewFieldLengths:
    """
    Field length constants for review-related data.
    
    These constants ensure that review data meets database constraints
    and provides a good user experience. The MAX_COMMENT_LENGTH is
    set to 300 characters to allow detailed reviews while preventing
    excessively long comments that could impact performance.
    """
    # Maximum length for review comments in characters
    # This balances allowing detailed feedback with preventing abuse
    MAX_COMMENT_LENGTH = 300


class InventoryFiledLengths:
    """
    Field length constants for inventory pricing data.
    
    These constants ensure that price data is stored consistently
    and accurately. The decimal places and max digits are set to
    handle typical jewelry pricing while preventing overflow.
    """
    # Maximum number of digits for price (including decimal places)
    # Allows prices up to 99999.99 (5 digits + 2 decimal places)
    PRICE_MAX_DIGITS = 7
    
    # Number of decimal places for price storage
    # Standard for currency (e.g., $150.00, $1,299.99)
    PRICE_DECIMAL_PLACES = 2


class ReviewErrorMessages:
    """
    User-friendly error messages for review operations.
    
    These messages provide clear feedback when review operations fail,
    helping users understand what went wrong and how to fix it.
    """
    # Error message when content type or object ID is invalid
    # This occurs when trying to review a non-existent product
    ERROR_INVALID_CONTENT_TYPE_OR_ID = 'Invalid content type or object ID'
    
    # Error message when a specific review cannot be found
    # This occurs when trying to access a review that doesn't exist
    ERROR_REVIEW_NOT_FOUND = 'Review not found'


class NameFieldLengths:
    """
    Standard name field length for various entities.
    
    This constant ensures consistency across all name fields in the
    application. The 30-character limit provides enough space for
    descriptive names while maintaining database efficiency.
    """
    # Maximum length for name fields across the application
    # Used for collections, colors, metals, stones, sizes, etc.
    NAME_MAX_LENGTH = 30
