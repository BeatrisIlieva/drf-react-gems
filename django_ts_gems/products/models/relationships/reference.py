from django.db import models

from django_ts_gems.products.choices import ReferenceChoices


class Reference(models.Model):
    name = models.CharField(
        max_length=ReferenceChoices.max_length(),
        choices=ReferenceChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This reference already exists.'
        }
    )

    def __str__(self):
        return self.name
