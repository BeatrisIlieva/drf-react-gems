from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

UserModel = get_user_model()


class Payment(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    card_holder = models.CharField(
        max_length=100,
        # Please enter the name as it appears on the credit card.
    )

    card_number = models.CharField(
        validators=[
            RegexValidator(regex=r'^\d{16}$',
                           message='Please enter a valid 16 digit card number'),
        ],
    )

    expiry_date = models.CharField(
        validators=[
            RegexValidator(regex=r'^(0[1-9]|1[0-2])\/\d{2}$',
                           message='Please enter a valid expiry date'),
        ],
    )

    cvv_code = models.CharField(
        validators=[
            RegexValidator(regex=r'^\d{3}$',
                           message='Please enter your card’s 3-digit security code'),
        ],
    )
