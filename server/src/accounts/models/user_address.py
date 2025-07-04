from django.core.validators import MinLengthValidator
from src.accounts.validators.models import NameValidator
from django.contrib.auth import get_user_model
from django.db import models
from src.accounts.constants import UserFieldLengths

UserModel = get_user_model()


class UserAddress(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
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
