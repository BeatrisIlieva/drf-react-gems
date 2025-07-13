"""
User Credential Model for DRF React Gems E-commerce Platform

This module defines the custom user model for the e-commerce application.
Instead of using Django's default User model, we create a custom one that
extends AbstractBaseUser and PermissionsMixin to provide enhanced functionality.

The custom user model allows us to:
- Use email as the primary identifier instead of username
- Add custom fields like agreed_to_emails
- Implement custom validation and business logic
- Maintain full compatibility with Django's authentication system
"""

# Django authentication imports for custom user model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Local imports for custom functionality
from src.accounts.managers import UserCredentialManager
from src.accounts.validators.models import UsernameValidator
from src.accounts.constants import UserFieldLengths, UserErrorMessages


class UserCredential(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the e-commerce application.
    
    This model extends Django's AbstractBaseUser and PermissionsMixin to create
    a fully functional custom user model. It uses email as the primary identifier
    instead of username, which is more common in modern web applications.
    
    Key Features:
    - Email-based authentication (no username required for login)
    - Custom username field with validation
    - Email marketing consent tracking
    - Full Django admin and permission system compatibility
    
    Inheritance:
    - AbstractBaseUser: Provides basic user functionality (password, last_login, etc.)
    - PermissionsMixin: Provides permission and group functionality
    """
    
    # Email field as the primary identifier
    # unique=True ensures no two users can have the same email
    # This is the field used for authentication (USERNAME_FIELD)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': UserErrorMessages.EMAIL_UNIQUE,  # Custom error message
        }
    )

    # Username field for display purposes
    # max_length uses a constant for consistency across the application
    # unique=True ensures usernames are unique across all users
    # validators list includes custom username validation rules
    username = models.CharField(
        max_length=UserFieldLengths.USERNAME_MAX,  # Defined in constants
        unique=True,
        validators=[
            UsernameValidator(),  # Custom validator for username format
        ],
        error_messages={
            'unique': UserErrorMessages.USERNAME_UNIQUE,  # Custom error message
        }
    )

    # Standard Django user fields
    # is_active controls whether the user can log in
    # is_staff controls access to Django admin
    is_active = models.BooleanField(
        default=True,  # Users are active by default
    )

    is_staff = models.BooleanField(
        default=False,  # Users are not staff by default
    )

    # Custom field for email marketing consent
    # This tracks whether the user has agreed to receive marketing emails
    # Important for GDPR compliance and email marketing campaigns
    agreed_to_emails = models.BooleanField(
        default=False,  # Users must explicitly opt-in to emails
    )

    # Custom manager for user creation and queries
    # UserCredentialManager provides custom methods for user management
    objects = UserCredentialManager()

    # Django authentication configuration
    # USERNAME_FIELD tells Django which field to use for authentication
    # In this case, users log in with their email address
    USERNAME_FIELD = 'email'
    
    # REQUIRED_FIELDS specifies which fields are required when creating a superuser
    # These fields will be prompted for during createsuperuser command
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        String representation of the user model.
        
        Returns the email address as the string representation.
        This is used in Django admin, shell, and debugging.
        
        Returns:
            str: The user's email address
        """
        return self.email
