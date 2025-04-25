from django.utils.translation import gettext_lazy as _
from django.db import models

from djangoTSGems.products.mixins import ChoicesMaxLengthMixin


class Material(models.Model):

    class TitleChoices(ChoicesMaxLengthMixin, models.TextChoices):
        YELLOW_GOLD = "YG", _("Yellow Gold")
        ROSE_GOLD = "RG", _("Rose Gold")
        STERLING_SILVER = "ST", _("Sterling Silver")

    title = models.CharField(
        max_length=TitleChoices.max_length(),
        choices=TitleChoices.choices,
    )

    def __str__(self):
        return self.get_title_display()
