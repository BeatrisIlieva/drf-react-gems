from django.db import models

from djangoTSGems.addresses.models.state import State


class City(models.Model):
    
    name = models.CharField(
        max_length=100,
    )

    state = models.ForeignKey(
        to=State,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
