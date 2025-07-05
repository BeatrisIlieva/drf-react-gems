from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django.db import models

from src.accounts.validators.models import (
    OnlyDigitsValidator,
    NameValidator
)
from src.accounts.constants import UserFieldLengths

UserModel = get_user_model()


class UserProfile(models.Model):
    first_name = models.CharField(
        max_length=UserFieldLengths.FIRST_NAME_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.FIRST_NAME_MIN),
            NameValidator(),
        ],
        null=True,
        blank=False,
    )

    last_name = models.CharField(
        max_length=UserFieldLengths.LAST_NAME_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.LAST_NAME_MIN),
            NameValidator(),
        ],
        null=True,
        blank=False,
    )

    phone_number = models.CharField(
        max_length=UserFieldLengths.PHONE_NUMBER_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.PHONE_NUMBER_MIN),
            OnlyDigitsValidator(),
        ],
        null=True,
        blank=False,
    )

    country = models.CharField(
        max_length=UserFieldLengths.COUNTRY_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.COUNTRY_MIN),
            NameValidator(),
        ],
        null=True,
        blank=False,
    )

    city = models.CharField(
        max_length=UserFieldLengths.CITY_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.CITY_MIN),
            NameValidator(),
        ],
        null=True,
        blank=False,
    )

    zip_code = models.CharField(
        max_length=UserFieldLengths.ZIP_CODE_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.ZIP_CODE_MIN),
        ],
        null=True,
        blank=False,
    )

    street_address = models.CharField(
        max_length=UserFieldLengths.STREET_ADDRESS_MAX,
        validators=[
            MinLengthValidator(UserFieldLengths.STREET_ADDRESS_MIN),
        ],
        null=True,
        blank=False,
    )

    apartment = models.CharField(
        max_length=UserFieldLengths.APARTMENT_MAX,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
