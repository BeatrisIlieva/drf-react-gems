"""
Comment Validator for Review Model

This module provides a custom validator for the Review model's comment field
to enforce the max_length constraint at the model level, ensuring data integrity
and consistent validation behavior across the application.

The validator is used to prevent excessively long comments from being saved
to the database, maintaining consistent comment length limits throughout the system.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from src.products.constants import ReviewFieldLengths


def validate_comment_length(value):
    """
    Custom validator to enforce max_length for Review comment field.
    
    This validator ensures that comment text doesn't exceed the maximum
    allowed length defined in ReviewFieldLengths.MAX_COMMENT_LENGTH.
    
    Django's TextField doesn't enforce max_length at the model level,
    so this validator provides the missing validation to prevent
    data integrity issues and ensure consistent behavior.
    
    Args:
        value (str): The comment text to validate
        
    Raises:
        ValidationError: If the comment exceeds the maximum allowed length
        
    Example:
        # In Review model:
        comment = models.TextField(
            max_length=ReviewFieldLengths.MAX_COMMENT_LENGTH,
            validators=[validate_comment_length],
            blank=False,
        )
    """
    # Check if the comment length exceeds the maximum allowed length
    if len(value) > ReviewFieldLengths.MAX_COMMENT_LENGTH:
        # Create a user-friendly error message
        error_message = _(
            f'Comment cannot exceed {ReviewFieldLengths.MAX_COMMENT_LENGTH} characters. '
            f'Current length: {len(value)} characters.'
        )
        
        # Raise ValidationError with the custom message
        # This will be displayed to users and logged for debugging
        raise ValidationError(error_message)
    
    # If validation passes, the function returns None (implicitly)
    # Django will continue with the normal save process 