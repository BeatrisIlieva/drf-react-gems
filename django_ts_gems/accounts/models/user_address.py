from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class UserAddress(models.Model):
    APARTMENT_MAX_LENGTH = 20

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    apartment = models.CharField(
        max_length=APARTMENT_MAX_LENGTH,
        null=True,
        blank=True,
    )

    state = models.ForeignKey(
        to='State',
        on_delete=models.CASCADE,
    )

    city = models.ForeignKey(
        to='City',
        on_delete=models.CASCADE,
    )

    street_address = models.ForeignKey(
        to='StreetAddress',
        on_delete=models.CASCADE,
    )

    zip_code = models.ForeignKey(
        to='ZipCode',
        on_delete=models.CASCADE,
    )
