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
