from django.db import models

from src.products.choices import MaterialChoices


class Material(models.Model):

    name = models.CharField(
        max_length=MaterialChoices.max_length(),
        choices=MaterialChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This material already exists.'
        }
    )

    def __str__(self):
        return self.name
