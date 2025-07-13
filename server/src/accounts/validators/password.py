"""
Custom Password Validators for DRF React Gems E-commerce Platform

This module contains custom Django password validators that enforce strong
password requirements. These validators ensure users create secure passwords
by checking for various character types and patterns.

The validators follow Django's password validation framework and provide:
- Clear error messages for each validation failure
- Help text for user guidance
- Internationalization support
- Integration with Django's password validation system

Validators included:
- DigitRequiredValidator: Ensures password contains at least one digit
- UpperCaseLetterRequiredValidator: Ensures password contains uppercase letters
- LowerCaseLetterRequiredValidator: Ensures password contains lowercase letters
- NoWhiteSpacesRequiredValidator: Prevents whitespace in passwords
- SpecialCharRequiredValidator: Ensures password contains special characters
"""

# Type hints for better code documentation and IDE support
from typing import Any, Optional
# Django imports for validation and internationalization
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class DigitRequiredValidator:
    """
    Password validator that requires at least one digit.
    
    This validator ensures that passwords contain at least one numeric
    character (0-9). This is a common security requirement that makes
    passwords harder to guess or crack.
    
    The validator follows Django's password validation framework and
    provides internationalized error messages and help text.
    """
    
    def validate(
        self,
        password: str,
        user: Optional[Any] = None
    ) -> None:
        """
        Validate that the password contains at least one digit.
        
        This method is called by Django's password validation system
        when a user sets or changes their password. It checks if the
        password contains at least one numeric character.
        
        Args:
            password: The password string to validate
            user: The user object (not used in this validator)
            
        Raises:
            ValidationError: If the password doesn't contain any digits
        """
        # Check if any character in the password is a digit
        # any() returns True if at least one character is a digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_digit',  # Unique error code for this validator
            )

    def get_error_message(self) -> str:
        """
        Get the error message for validation failure.
        
        Returns:
            str: Internationalized error message
        """
        return _("Your password must contain at least one digit.")

    def get_help_text(self) -> str:
        """
        Get the help text for this validator.
        
        This text is displayed to users to explain the password requirements.
        
        Returns:
            str: Internationalized help text
        """
        return _("Your password must contain at least one digit.")


class UpperCaseLetterRequiredValidator:
    """
    Password validator that requires at least one uppercase letter.
    
    This validator ensures that passwords contain at least one uppercase
    letter (A-Z). This is a common security requirement that makes
    passwords harder to guess or crack.
    """
    
    def validate(
        self,
        password: str,
        user: Optional[Any] = None
    ) -> None:
        """
        Validate that the password contains at least one uppercase letter.
        
        Args:
            password: The password string to validate
            user: The user object (not used in this validator)
            
        Raises:
            ValidationError: If the password doesn't contain any uppercase letters
        """
        # Check if any character in the password is an uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_upper_case_letter',
            )

    def get_error_message(self) -> str:
        """
        Get the error message for validation failure.
        
        Returns:
            str: Internationalized error message
        """
        return _("Your password must contain at least one upper case letter.")

    def get_help_text(self) -> str:
        """
        Get the help text for this validator.
        
        Returns:
            str: Internationalized help text
        """
        return _("Your password must contain at least one upper case letter.")


class LowerCaseLetterRequiredValidator:
    """
    Password validator that requires at least one lowercase letter.
    
    This validator ensures that passwords contain at least one lowercase
    letter (a-z). This is a common security requirement that makes
    passwords harder to guess or crack.
    """
    
    def validate(
        self,
        password: str,
        user: Optional[Any] = None
    ) -> None:
        """
        Validate that the password contains at least one lowercase letter.
        
        Args:
            password: The password string to validate
            user: The user object (not used in this validator)
            
        Raises:
            ValidationError: If the password doesn't contain any lowercase letters
        """
        # Check if any character in the password is a lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_lower_case_letter',
            )

    def get_error_message(self) -> str:
        """
        Get the error message for validation failure.
        
        Returns:
            str: Internationalized error message
        """
        return _("Your password must contain at least one lower case letter.")

    def get_help_text(self) -> str:
        """
        Get the help text for this validator.
        
        Returns:
            str: Internationalized help text
        """
        return _("Your password must contain at least one lower case letter.")


class NoWhiteSpacesRequiredValidator:
    """
    Password validator that prevents whitespace characters.
    
    This validator ensures that passwords don't contain any whitespace
    characters (spaces, tabs, newlines). This prevents common issues
    with password handling and ensures consistent password format.
    """
    
    def validate(
        self,
        password: str,
        user: Optional[Any] = None
    ) -> None:
        """
        Validate that the password doesn't contain any whitespace characters.
        
        Args:
            password: The password string to validate
            user: The user object (not used in this validator)
            
        Raises:
            ValidationError: If the password contains whitespace characters
        """
        # Check if any character in the password is a whitespace
        if any(char.isspace() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_white_spaces',
            )

    def get_error_message(self) -> str:
        """
        Get the error message for validation failure.
        
        Returns:
            str: Internationalized error message
        """
        return _("Your password must not contain white spaces.")

    def get_help_text(self) -> str:
        """
        Get the help text for this validator.
        
        Returns:
            str: Internationalized help text
        """
        return _("Your password must not contain white spaces.")


class SpecialCharRequiredValidator:
    """
    Password validator that requires at least one special character.
    
    This validator ensures that passwords contain at least one special
    character from the set: !#$%. This makes passwords more secure
    by increasing the character set used.
    
    The allowed special characters are limited to common, safe characters
    that work well across different systems and input methods.
    """
    
    def validate(
        self,
        password: str,
        user: Optional[Any] = None
    ) -> None:
        """
        Validate that the password contains at least one special character.
        
        Args:
            password: The password string to validate
            user: The user object (not used in this validator)
            
        Raises:
            ValidationError: If the password doesn't contain any special characters
        """
        # Define the allowed special characters
        special_chars = '!#$%'
        
        # Check if any character in the password is in the special characters set
        if not any(char in special_chars for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_special_char',
            )

    def get_error_message(self) -> str:
        """
        Get the error message for validation failure.
        
        Returns:
            str: Internationalized error message
        """
        return _("Your password must contain at least one special character (!#$%)")

    def get_help_text(self) -> str:
        """
        Get the help text for this validator.
        
        Returns:
            str: Internationalized help text
        """
        return _("Your password must contain at least one special character (!#$%)")
