from django.db import models


class State(models.Model):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name
