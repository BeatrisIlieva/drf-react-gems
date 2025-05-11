from django.db import models

from src.addresses.models.state import State


class City(models.Model):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    state = models.ForeignKey(
        to=State,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
