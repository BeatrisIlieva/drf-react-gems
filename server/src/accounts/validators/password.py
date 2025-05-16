from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class DigitRequiredValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Your password must contain at least one digit."),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _("Your password must contain at least one digit.")


class UpperCaseLetterRequiredValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Your password must contain at least one upper case letter."),
                code='password_no_upper_case_letter',
            )

    def get_help_text(self):
        return _("Your password must contain at least one upper case letter.")


class LowerCaseLetterRequiredValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Your password must contain at least one lower case letter."),
                code='password_no_lower_case_letter',
            )

    def get_help_text(self):
        return _("Your password must contain at least one lower case letter.")


class NoWhiteSpacesRequiredValidator:
    def validate(self, password, user=None):
        if any(char.isspace() for char in password):
            raise ValidationError(
                _("Your password must not contain white spaces."),
                code='password_no_white_spaces',
            )

    def get_help_text(self):
        return _("Your password must not contain white spaces.")


class SpecialCharRequiredValidator:
    def validate(self, password, user=None):
        special_chars = '!#$%'
        if not any(char in special_chars for char in password):
            raise ValidationError(
                _("Your password must contain at least one special character (!#$%)"),
                code='password_no_special_char',
            )

    def get_help_text(self):
        return _("Your password must contain at least one special character (!#$%)")
