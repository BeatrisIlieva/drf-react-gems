"""
This module contains custom Django password validators.

Validators included:
- DigitRequiredValidator: Ensures password contains at least one digit
- UpperCaseLetterRequiredValidator: Ensures password contains uppercase letters
- LowerCaseLetterRequiredValidator: Ensures password contains lowercase letters
- NoWhiteSpacesRequiredValidator: Prevents whitespace in passwords
- SpecialCharRequiredValidator: Ensures password contains special characters
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from src.accounts.constants import UserErrorMessages


class DigitRequiredValidator:
    """
    Validate that the password contains at least one digit.

    This method is called by Django's password validation system
    when a user sets or changes their password. It checks if the
    password contains at least one numeric character.
    """

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_digit'
            )

    def get_error_message(self):

        return _(UserErrorMessages.PASSWORD_NO_DIGIT)

    def get_help_text(self):

        return _(UserErrorMessages.PASSWORD_NO_DIGIT)


class UpperCaseLetterRequiredValidator:
    """
    Password validator that requires at least one uppercase letter.

    This validator ensures that passwords contain at least one uppercase
    letter (A-Z). 
    """

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_upper_case_letter'
            )

    def get_error_message(self):

        return _(UserErrorMessages.PASSWORD_NO_UPPER_CASE_LETTER)

    def get_help_text(self):

        return _(UserErrorMessages.PASSWORD_NO_UPPER_CASE_LETTER)


class LowerCaseLetterRequiredValidator:
    """
    Password validator that requires at least one lowercase letter.

    This validator ensures that passwords contain at least one lowercase
    letter (a-z). This is a common security requirement that makes
    passwords harder to guess or crack.
    """

    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_lower_case_letter'
            )

    def get_error_message(self):

        return _(UserErrorMessages.PASSWORD_NO_LOWER_CASE_LETTER)

    def get_help_text(self):

        return _(UserErrorMessages.PASSWORD_NO_LOWER_CASE_LETTER)


class NoWhiteSpacesRequiredValidator:
    """
    Password validator that prevents whitespace characters.

    This validator ensures that passwords don't contain any whitespace
    characters. 
    """

    def validate(self, password, user=None):
        if any(char.isspace() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_white_spaces'
            )

    def get_error_message(self):

        return _(UserErrorMessages.PASSWORD_NO_WHITE_SPACES)

    def get_help_text(self):

        return _(UserErrorMessages.PASSWORD_NO_WHITE_SPACES)


class SpecialCharRequiredValidator:
    """
    Password validator that requires at least one special character.

    This validator ensures that passwords contain at least one special
    character from the set: !#$%. 
    """

    def validate(self, password, user=None):
        special_chars = '!#$%'

        if not any(char in special_chars for char in password):
            raise ValidationError(
                self.get_error_message(),
                code='password_no_special_char'
            )

    def get_error_message(self):

        return _(UserErrorMessages.PASSWORD_NO_SPECIAL_CHAR)

    def get_help_text(self):

        return _(UserErrorMessages.PASSWORD_NO_SPECIAL_CHAR)
