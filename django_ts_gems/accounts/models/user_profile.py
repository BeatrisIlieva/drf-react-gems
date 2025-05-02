from django.core.validators import MinLengthValidator
from django.db import models

from django_ts_gems.accounts.admin import UserModel
from django_ts_gems.accounts.validators import (
    OnlyDigitsValidator,
    NameValidator
)


class UserProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30
    PHONE_NUMBER_MAX_LENGTH = 15
    PHONE_NUMBER_MIN_LENGTH = 9

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            NameValidator(),
        ],
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            NameValidator(),
        ],
    )

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=[
            MinLengthValidator(PHONE_NUMBER_MIN_LENGTH),
            OnlyDigitsValidator(),
        ],
    )
