from django.db import models

from django_ts_gems.products.choices import CollectionChoices


class Collection(models.Model):

    name = models.CharField(
        max_length=CollectionChoices.max_length(),
        choices=CollectionChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This collection already exists.'
        }
    )
