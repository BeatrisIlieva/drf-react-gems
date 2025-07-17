"""
The UserIdentificationService handles user identification for both authenticated
and anonymous (guest) users, which is essential for shopping cart and wishlist
functionality.
"""

from rest_framework.exceptions import ValidationError

import uuid


class UserIdentificationService:
    """
    Service class for identifying users in the e-commerce application.

    For authenticated users, it returns the user object.
    For anonymous users, it validates and returns a guest ID from the request headers.
    """

    @staticmethod
    def get_user_identifier(request):
        # Check if the user is authenticated (logged in)
        if request.user.is_authenticated:
            # Return the authenticated user object
            # This is used throughout the app to identify the user
            return {'user': request.user}

        # For anonymous (guest) users, get the Guest-Id from request headers
        # The Guest-Id is set by the React frontend for guest users
        guest_id = request.headers.get('Guest-Id')
        if not guest_id:
            # If no Guest-Id is provided, raise a validation error
            # This ensures guest users can't use features without proper identification
            raise ValidationError(
                {'guest_id': 'Guest-Id header is required for anonymous users'})

        try:
            # Convert the string guest ID to a UUID object
            # UUID validation ensures the guest ID is in the correct format
            guest_uuid = uuid.UUID(guest_id)

            # Return the validated guest ID
            return {'guest_id': guest_uuid}

        except (ValueError, TypeError):
            # If the guest ID is not a valid UUID format, raise validation error
            # This prevents invalid guest IDs from being used
            raise ValidationError({'guest_id': 'Invalid guest ID format'})
