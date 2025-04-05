from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator

UserModel = get_user_model()


class Contact(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
    )

    last_name = models.CharField(
        max_length=30,
    )

    phone_number = models.CharField(
        validators=[
            RegexValidator(regex=r'^\+?\d{9,15}$',
                           message='Please enter a valid 16 digit card number'),
        ],
    )

    country = models.CharField(
        max_length=50,
    )

    city = models.CharField(
        max_length=100,
    )

    street_address = models.CharField(
        max_length=255,
    )

    apartment = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
    )
