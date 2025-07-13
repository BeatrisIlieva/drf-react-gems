"""
Custom Authentication Backend for DRF React Gems E-commerce Platform

This module defines a custom authentication backend that extends Django's
ModelBackend to provide enhanced authentication capabilities. The custom backend
allows users to authenticate using either their email address or username,
providing flexibility in the login process.

The CustomAuthBackendBackend:
- Allows authentication with email OR username
- Maintains compatibility with Django's authentication system
- Provides case-insensitive authentication
- Integrates with Django's permission system
"""

# Type hints for better code documentation and IDE support
from typing import Any, Optional
# Django authentication imports
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest

# Get the active user model (our custom UserCredential)
UserModel = get_user_model()


class CustomAuthBackendBackend(ModelBackend):
    """
    Custom authentication backend for flexible user authentication.
    
    This backend extends Django's ModelBackend to allow users to authenticate
    using either their email address or username. This provides a better user
    experience as users can log in with whichever identifier they prefer.
    
    Features:
    - Email or username authentication
    - Case-insensitive authentication
    - Full compatibility with Django's permission system
    - Integration with Django's authentication framework
    
    The backend is configured in settings.py and used by Django's
    authentication system for login validation.
    """
    
    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[Any]:
        """
        Authenticate a user using email or username.
        
        This method is called by Django's authentication system when a user
        attempts to log in. It checks if the provided credentials match
        a user in the database.
        
        The method supports authentication with either email or username,
        making it flexible for users who might prefer one over the other.
        
        Args:
            request: The HTTP request object (can be None for some auth methods)
            username: The username or email provided by the user
            password: The password provided by the user
            **kwargs: Additional keyword arguments (not used in this implementation)
        
        Returns:
            UserCredential object if authentication succeeds, None otherwise
            
        Example:
            # User can authenticate with email
            user = backend.authenticate(request, username='user@example.com', password='password')
            
            # Or with username
            user = backend.authenticate(request, username='john_doe', password='password')
        """
        try:
            # Try to find a user with the provided username/email
            # Q objects allow for complex queries with OR conditions
            # email__iexact=username: Match email case-insensitively
            # username__iexact=username: Match username case-insensitively
            # The | operator creates an OR condition between the two queries
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            # If no user is found with the provided credentials, return None
            # This indicates authentication failure
            return None
        
        # Check if the provided password is correct and user can authenticate
        # check_password() securely compares the provided password with the stored hash
        # user_can_authenticate() checks if the user is active and not blocked
        if user.check_password(password) and self.user_can_authenticate(user):
            # Return the authenticated user object
            return user
        
        # Return None if password is incorrect or user cannot authenticate
        return None
