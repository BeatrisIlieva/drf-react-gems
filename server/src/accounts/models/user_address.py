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
        to='accounts.State',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    city = models.ForeignKey(
        to='accounts.City',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    street_address = models.ForeignKey(
        to='accounts.StreetAddress',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    zip_code = models.ForeignKey(
        to='accounts.ZipCode',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )


class State(models.Model):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class City(models.Model):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    state = models.ForeignKey(
        to='accounts.State',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    ZIP_CODE_MAX_LENGTH = 20

    zip_code = models.CharField(
        max_length=ZIP_CODE_MAX_LENGTH,
    )

    city = models.ForeignKey(
        to='accounts.City',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.zip_code


class StreetAddress(models.Model):
    STREET_ADDRESS_MAX_LENGTH = 200

    street_address = models.CharField(
        max_length=STREET_ADDRESS_MAX_LENGTH,
    )

    zip_code = models.ForeignKey(
        to='accounts.ZipCode',
        on_delete=models.CASCADE,
    )
