from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


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
