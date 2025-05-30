from django.db import models

from src.addresses.models.zip_code import ZipCode


class StreetAddress(models.Model):
    STREET_ADDRESS_MAX_LENGTH = 200

    street_address = models.CharField(
        max_length=STREET_ADDRESS_MAX_LENGTH,
    )

    zip_code = models.ForeignKey(
        to=ZipCode,
        on_delete=models.CASCADE,
    )
