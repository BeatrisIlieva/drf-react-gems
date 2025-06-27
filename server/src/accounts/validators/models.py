from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as DjangoEmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
import re


@deconstructible
class OnlyDigitsValidator:
    DEFAULT_MESSAGE = 'This field can contain only digits.'

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = self.DEFAULT_MESSAGE

    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError(self.__message)


@deconstructible
class NameValidator:
    DEFAULT_MESSAGE = 'This field can contain only letters, hyphens, apostrophes and spaces.'

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = self.DEFAULT_MESSAGE

    def __call__(self, value):
        normalized = value.replace("’", "'")

        for char in normalized:
            if not (
                    char.isalpha() or
                    char in "'-" or
                    char.isspace()
            ):

                raise ValidationError(self.__message)


@deconstructible
class UsernameValidator:
    DEFAULT_MESSAGE = 'Username must be 3-30 characters long and contain only letters, numbers, and underscores.'

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        # Username validation: 3-30 characters, letters, numbers, underscores only
        if not re.match(r'^[A-Za-z0-9_]{3,30}$', value):
            raise ValidationError(self.__message)


@deconstructible
class EmailOrUsernameValidator:
    DEFAULT_MESSAGE = 'Please enter a valid email address or username.'

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = self.DEFAULT_MESSAGE
        else:
            self.__message = value

    def __call__(self, value):
        # Check if it's a valid email using Django's built-in validator
        django_email_validator = DjangoEmailValidator()
        is_email = False
        try:
            django_email_validator(value)
            is_email = True
        except ValidationError:
            pass
        
        # Check if it's a valid username
        is_username = re.match(r'^[A-Za-z0-9_]{3,30}$', value)
        
        if not (is_email or is_username):
            raise ValidationError(self.__message)
