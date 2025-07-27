"""
This module defines the custom user model for the e-commerce application.
Instead of using Django's default User model, we create a custom one that
extends AbstractBaseUser and PermissionsMixin.

The custom user model allows us to:
- Use email as the primary identifier instead of username
- Add custom fields like agreed_to_emails
- Implement custom validation and business logic
"""

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from src.accounts.managers import UserCredentialManager
from src.accounts.validators.models import UsernameValidator
from src.accounts.constants import UserFieldLengths, UserErrorMessages


class UserCredential(AbstractBaseUser, PermissionsMixin):

    # Email field as the primary identifier
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': UserErrorMessages.EMAIL_UNIQUE,  # Custom error message
        },
    )

    # Username field for display purposes
    username = models.CharField(
        max_length=UserFieldLengths.USERNAME_MAX,  # Defined in constants
        unique=True,
        validators=[
            UsernameValidator(),  # Custom validator for username format
        ],
        error_messages={
            'unique': UserErrorMessages.USERNAME_UNIQUE,  # Custom error message
        },
    )

    # This tracks whether the user has agreed to receive marketing emails
    agreed_to_emails = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    # Custom manager for user creation and queries
    objects = UserCredentialManager()

    # USERNAME_FIELD tells Django which field to use for authentication
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS specifies which fields are required when creating an user
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
