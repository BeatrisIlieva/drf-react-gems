from django.db import models

from src.products.choices import SizeChoices


class Size(models.Model):

    size = models.CharField(
        max_length=SizeChoices.max_length(),
        choices=SizeChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This size already exists.'
        }
    )

    def __str__(self):
        return self.size
