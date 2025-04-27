
from django.db import models


class PrimaryStone(models.Model):
    NAME_MAX_LENGTH = 30

    primary_stone = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        error_messages={
            'unique': 'This primary stone already exists.'
        }
    )

    image = models.URLField()
