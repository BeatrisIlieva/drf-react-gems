"""
This module contains custom Django validators for model field validation.

The validators use the @deconstructible decorator to make them serializable
for Django migrations and form handling.

Validators included:
- OnlyDigitsValidator: Ensures field contains only numeric characters
- NameValidator: Validates proper name format (letters, hyphens, apostrophes, spaces)
- UsernameValidator: Validates username format (letters, numbers, underscores, 3-30 chars)
- EmailOrUsernameValidator: Validates either email or username format
"""

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as DjangoEmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

import re


@deconstructible
class OnlyDigitsValidator:
    """
    Validator that ensures a field contains only numeric characters.

    This validator is used for fields like phone numbers where only
    digits are allowed.
    """

    # Default error message for this validator
    DEFAULT_MESSAGE = 'This field can contain only digits.'

    def __init__(self, message=None):
        """
        Initialize the validator with an optional custom message.
        """
        self.message = message

    @property
    def message(self):
        """
        Get the current error message.
        """
        return self.__message

    @message.setter
    def message(self, value=None):
        """
        Set the error message, using default if None is provided.
        """
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        """
        Validate that the value contains only digits.

        This method is called by Django's validation system when
        the field is validated. It checks if the string contains
        only numeric characters.
        """
        if not value.isdigit():
            raise ValidationError(self.__message)


@deconstructible
class NameValidator:
    """
    Validator that ensures a field contains only valid name characters.

    This validator is used for name fields (first name, last name, city, country)
    and allows letters, hyphens, apostrophes, and spaces.
    """

    # Default error message for this validator
    DEFAULT_MESSAGE = (
        'This field can contain only letters, hyphens, apostrophes and spaces.'
    )

    def __init__(self, message=None):
        """
        Initialize the validator with an optional custom message.
        """
        self.message = message

    @property
    def message(self):
        """
        Get the current error message.
        """
        return self.__message

    @message.setter
    def message(self, value=None):
        """
        Set the error message, using default if None is provided.
        """
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        """
        Validate that the value contains only valid name characters.

        This method normalizes different types of apostrophes and then
        checks each character to ensure it's a letter, hyphen, apostrophe,
        or space.
        """
        normalized = value.replace("'", "'")

        for char in normalized:
            if not (char.isalpha() or char in "'-" or char.isspace()):
                raise ValidationError(self.__message)


@deconstructible
class UsernameValidator:
    """
    Validator that ensures a username follows proper format rules.

    This validator ensures usernames are 3-30 characters long and contain
    only letters, numbers, and underscores.
    """

    # Default error message for this validator
    DEFAULT_MESSAGE = 'Username must be 3-30 characters long and contain only letters, numbers, and underscores.'

    def __init__(self, message=None):
        """
        Initialize the validator with an optional custom message.

        Args:
            message: Custom error message to use instead of default
        """
        self.message = message

    @property
    def message(self):
        """
        Get the current error message.

        Returns:
            str: The error message to display on validation failure
        """
        return self.__message

    @message.setter
    def message(self, value=None):
        """
        Set the error message, using default if None is provided.
        """
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        """
        Validate that the value follows username format rules.

        This method uses a regular expression to validate the username format:
        - 3-30 characters long
        - Only letters (a-z, A-Z), numbers (0-9), and underscores (_)

        Args:
            value: The string value to validate

        Raises:
            ValidationError: If the value doesn't match username format
        """
        if not re.match(r'^[A-Za-z0-9_]{3,30}$', value):
            raise ValidationError(self.__message)


@deconstructible
class EmailOrUsernameValidator:
    """
    Validator that accepts either a valid email address or username.

    This validator is used for login fields where users can enter either
    their email address or username. It first tries to validate as an email,
    then as a username if email validation fails.
    """

    # Default error message for this validator
    DEFAULT_MESSAGE = 'Please enter a valid email address or username.'

    def __init__(self, message=None):
        """
        Initialize the validator with an optional custom message.
        """
        self.message = message

    @property
    def message(self):
        """
        Get the current error message.
        """
        return self.__message

    @message.setter
    def message(self, value=None):
        """
        Set the error message, using default if None is provided.
        """
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        """
        Validate that the value is either a valid email or username.

        This method first tries to validate the value as an email address
        using Django's built-in EmailValidator. If that fails, it tries
        to validate as a username using the same regex pattern as UsernameValidator.
        """
        django_email_validator = DjangoEmailValidator()

        is_email = False

        try:
            django_email_validator(value)
            is_email = True
        except ValidationError:
            pass

        is_username = re.match(r'^[A-Za-z0-9_]{3,30}$', value)

        if not (is_email or is_username):
            raise ValidationError(self.__message)
