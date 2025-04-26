from django.db import models

from djangoTSGems.products.choices import SizeChoices


class Size(models.Model):

    size = models.CharField(
        max_length=SizeChoices.max_length(),
        choices=SizeChoices.choices,
    )

    def __str__(self):
        return self.get_size_display()
