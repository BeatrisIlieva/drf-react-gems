from django.db import models

from django_ts_gems.products.choices import StoneChoices


class Stone(models.Model):

    name = models.CharField(
        max_length=StoneChoices.max_length(),
        choices=StoneChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This stone already exists.'
        }
    )

    image = models.URLField()

    def __str__(self):
        return self.name
