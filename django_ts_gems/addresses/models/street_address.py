from django.db import models

from django_ts_gems.addresses.models.zip_code import ZipCode


class StreetAddress(models.Model):

    street_address = models.CharField(
        max_length=200,
    )

    zip_code = models.ForeignKey(
        to=ZipCode,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.street}, {self.zip_code}"
