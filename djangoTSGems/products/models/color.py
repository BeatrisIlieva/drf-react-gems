from django.utils.translation import gettext_lazy as _
from django.db import models

from djangoTSGems.products.mixins import ChoicesMaxLengthMixin


class Color(models.Model):
    
    class TitleChoices(ChoicesMaxLengthMixin, models.TextChoices):
        AQUAMARINE = "AQ", _("Aquamarine")
        BLACK = "BL", _('Black')
        BLUE = "BU", _('Blue')
        GREEN = "GR", _('Green')
        PINK = "PI", _('Pink')
        RED = "RE", _('Red')
        WHITE = "WH", _('White')
        YELLOW = "YE", _('Yellow')

    title = models.CharField(
        max_length=TitleChoices.max_length(),
        choices=TitleChoices.choices,
    )

    image = models.URLField()
    
    def __str__(self):
        return self.get_title_display()
