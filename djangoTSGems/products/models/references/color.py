from django.db import models

from djangoTSGems.products.choices import ColorChoices


class Color(models.Model):

    color = models.CharField(
        max_length=ColorChoices.max_length(),
        choices=ColorChoices.choices,
    )

    image = models.URLField()

    def __str__(self):
        return self.get_color_display()
