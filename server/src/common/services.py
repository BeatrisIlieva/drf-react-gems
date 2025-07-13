"""
Common Services for DRF React Gems E-commerce Platform

This module contains service classes that provide business logic functionality
across different parts of the application. Services encapsulate complex operations
and can be reused by different views and serializers.

The UserIdentificationService handles user identification for both authenticated
and anonymous (guest) users, which is essential for shopping cart and wishlist
functionality.
"""

# DRF exception for handling validation errors
from rest_framework.exceptions import ValidationError

# Standard library imports
import uuid
from typing import Dict, Any, TYPE_CHECKING

# TYPE_CHECKING is used to avoid circular imports during runtime
# It only imports the type hints when type checking tools are running
if TYPE_CHECKING:
    from rest_framework.request import Request


class UserIdentificationService:
    """
    Service class for identifying users in the e-commerce application.
    
    This service handles both authenticated users and anonymous (guest) users.
    It's essential for features like shopping carts and wishlists that need
    to work for both logged-in users and guests.
    
    For authenticated users, it returns the user object.
    For anonymous users, it validates and returns a guest ID from the request headers.
    """
    
    @staticmethod
    def get_user_identifier(request: 'Request') -> Dict[str, Any]:
        """
        Get user identifier from the request, handling both authenticated and guest users.
        
        This method is the core of the user identification system. It checks if
        the user is authenticated and returns appropriate identification data.
        
        For authenticated users: returns the user object
        For guest users: validates the Guest-Id header and returns the guest ID
        
        Args:
            request: The HTTP request object containing user and header information
        
        Returns:
            Dict containing either:
            - {'user': user_object} for authenticated users
            - {'guest_id': uuid_object} for guest users
        
        Raises:
            ValidationError: If guest user doesn't provide Guest-Id header
                           or if the guest ID format is invalid
        
        Example:
            # For authenticated user
            {'user': <User: john_doe>}
            
            # For guest user
            {'guest_id': UUID('12345678-1234-5678-1234-567812345678')}
        """
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
