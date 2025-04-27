from django.db import models

from django_ts_gems.addresses.models.city import City


class ZipCode(models.Model):

    code = models.CharField(
        max_length=20,
    )

    city = models.ForeignKey(
        to=City,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.code
