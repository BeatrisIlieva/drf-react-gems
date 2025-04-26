from django.db import models

from djangoTSGems.products.choices import MaterialChoices


class Material(models.Model):

    material = models.CharField(
        max_length=MaterialChoices.max_length(),
        choices=MaterialChoices.choices,
    )

    def __str__(self):
        return self.get_material_display()
