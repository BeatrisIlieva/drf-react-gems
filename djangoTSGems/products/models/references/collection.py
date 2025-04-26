from django.db import models

from djangoTSGems.products.choices import CollectionChoices


class Collection(models.Model):

    collection = models.CharField(
        max_length=CollectionChoices.max_length(),
        choices=CollectionChoices.choices,
    )

    def __str__(self):
        return self.get_collection_display()
