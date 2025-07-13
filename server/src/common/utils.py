"""
Common Utilities for DRF React Gems E-commerce Platform

This module contains utility classes and functions that provide helper functionality
across the application. These utilities are designed to be reusable and solve
common programming problems.

The ChoicesMaxLengthMixin is a utility mixin for Django choice fields that
automatically calculates the maximum length needed for database storage.
"""

# Type hints for better code documentation and IDE support
from typing import Type, Any


class ChoicesMaxLengthMixin:
    """
    Mixin class for Django choice fields to automatically calculate max length.
    
    This mixin is used with Django choice fields to automatically determine
    the maximum length needed for database storage. It iterates through all
    choice values and finds the longest one.
    
    This is useful for ensuring database fields are properly sized and
    preventing data truncation issues.
    
    Usage:
        class ProductStatus(models.TextChoices, ChoicesMaxLengthMixin):
            ACTIVE = 'active', 'Active'
            INACTIVE = 'inactive', 'Inactive'
            
        # Then use max_length() to get the required field length
        max_len = ProductStatus.max_length()
    """
    
    @classmethod
    def max_length(cls: Type[Any]) -> int:
        """
        Calculate the maximum length needed for storing choice values.
        
        This method iterates through all choice values in the class and
        returns the length of the longest value. This is used to set
        the max_length parameter for Django model fields.
        
        Args:
            cls: The choice class (automatically passed by @classmethod)
        
        Returns:
            int: The length of the longest choice value
            
        Example:
            If choices are ['active', 'inactive', 'pending'], returns 8
            (length of 'inactive')
        """
        # Use a generator expression to find the maximum length
        # This is memory efficient as it doesn't create a list
        # len(choice.value) gets the length of each choice's value
        # max() finds the largest length among all choices
        return max(len(choice.value) for choice in cls)
