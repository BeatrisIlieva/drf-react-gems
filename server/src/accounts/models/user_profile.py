"""
User Profile Model for DRF React Gems E-commerce Platform

This module defines the UserProfile model which extends the user model with
additional personal and shipping information. This follows the common Django
pattern of having a separate profile model linked to the main user model.

The UserProfile model contains:
- Personal information (first name, last name, phone)
- Shipping address information (country, city, zip code, street address)
- One-to-one relationship with the main user model

This separation allows for flexible user data management and better data organization.
"""

# Django imports for model functionality and validation
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator

# Local imports for custom validators and constants
from src.accounts.validators.models import (
    OnlyDigitsValidator,
    NameValidator
)
from src.accounts.constants import UserFieldLengths

# Get the active user model (our custom UserCredential)
UserModel = get_user_model()


class UserProfile(models.Model):
    """
    User profile model containing additional user information.
    
    This model extends the main user model with personal and shipping information.
    It uses a one-to-one relationship with the user model, meaning each user
    can have exactly one profile and each profile belongs to exactly one user.
    
    The profile contains:
    - Personal information (name, phone)
    - Shipping address for order delivery
    - All fields are optional (null=True) but required when provided (blank=False)
    
    This design allows users to register with minimal information and complete
    their profile later, improving the user experience.
    """
    
    # Personal information fields
    # First name with custom validation for proper name format
    first_name = models.CharField(
        max_length=UserFieldLengths.FIRST_NAME_MAX,  # Maximum length from constants
        validators=[
            MinLengthValidator(UserFieldLengths.FIRST_NAME_MIN),  # Minimum length validation
            NameValidator(),  # Custom validator for name format (letters only)
        ],
        null=True,    # Can be NULL in database
        blank=False,  # Cannot be empty string in forms
    )

    # Last name with same validation as first name
    last_name = models.CharField(
        max_length=UserFieldLengths.LAST_NAME_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.LAST_NAME_MIN),
            NameValidator(),
        ],
        null=True,
        blank=False,
    )

    # Phone number with digit-only validation
    # OnlyDigitsValidator ensures only numbers are allowed
    phone_number = models.CharField(
        max_length=UserFieldLengths.PHONE_NUMBER_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.PHONE_NUMBER_MIN),
            OnlyDigitsValidator(),  # Custom validator for digits only
        ],
        null=True,
        blank=False,
    )

    # Shipping address fields
    # Country name with name validation
    country = models.CharField(
        max_length=UserFieldLengths.COUNTRY_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.COUNTRY_MIN),
            NameValidator(),  # Ensures proper country name format
        ],
        null=True,
        blank=False,
    )

    # City name with name validation
    city = models.CharField(
        max_length=UserFieldLengths.CITY_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.CITY_MIN),
            NameValidator(),  # Ensures proper city name format
        ],
        null=True,
        blank=False,
    )

    # ZIP/Postal code with only length validation
    # No format validation as ZIP codes vary by country
    zip_code = models.CharField(
        max_length=UserFieldLengths.ZIP_CODE_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.ZIP_CODE_MIN),
        ],
        null=True,
        blank=False,
    )

    # Street address with length validation
    # No format validation to allow various address formats
    street_address = models.CharField(
        max_length=UserFieldLengths.STREET_ADDRESS_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.STREET_ADDRESS_MIN),
        ],
        null=True,
        blank=False,
    )

    # Apartment/unit number (optional field)
    # This field is optional (blank=True) as not all addresses have apartment numbers
    apartment = models.CharField(
        max_length=UserFieldLengths.APARTMENT_MAX,
        null=True,
        blank=True,  # Can be empty in forms
    )

    # One-to-one relationship with the user model
    # primary_key=True makes this the primary key, creating a direct relationship
    # on_delete=models.CASCADE means if the user is deleted, the profile is also deleted
    # This ensures data consistency and prevents orphaned profile records
    user = models.OneToOneField(
        to=UserModel,           # Link to the custom user model
        on_delete=models.CASCADE,  # Delete profile when user is deleted
        primary_key=True,       # Use this field as the primary key
    )
