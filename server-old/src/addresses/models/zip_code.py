from django.db import models

from src.addresses.models.city import City


class ZipCode(models.Model):
    ZIP_CODE_MAX_LENGTH = 20

    zip_code = models.CharField(
        max_length=ZIP_CODE_MAX_LENGTH,
    )

    city = models.ForeignKey(
        to=City,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.code
