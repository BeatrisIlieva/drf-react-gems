from django.db import models

from django_ts_gems.products.choices import CollectionChoices


class Collection(models.Model):

    collection = models.CharField(
        max_length=CollectionChoices.max_length(),
        choices=CollectionChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This collection already exists.'
        }
    )

    def __str__(self):
        return self.get_collection_display()
