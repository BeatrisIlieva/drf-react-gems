from django.utils.translation import gettext_lazy as _
from django.db import models

from djangoTSGems.products.mixins import ChoicesMaxLengthMixin


class Size(models.Model):

    class SizeChoices(ChoicesMaxLengthMixin, models.TextChoices):
        XS = "XS", _("XS")
        S = "S", _("S")
        M = "M", _("M")
        L = "L", _("L")
        XL = "XL", _("XL")
        ONE_SIZE = 'OS', _('OS') 

    size = models.CharField(
        max_length=SizeChoices.max_length(),
        choices=SizeChoices.choices,
    )

    def __str__(self):
        return self.get_title_display()
