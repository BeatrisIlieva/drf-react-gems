from django.utils.translation import gettext_lazy as _
from django.db import models

from djangoTSGems.products.mixins import ChoicesMaxLengthMixin
from djangoTSGems.products.models.color import Color


class Stone(models.Model):

    class TitleChoices(ChoicesMaxLengthMixin, models.TextChoices):
        BLACK_SPINEL = 'BS', _('Spinel')
        DIAMOND = 'DI', _('Diamond')
        EMERALD = 'EM', _('Emerald')
        RUBY = 'RU', _('Ruby')
        SAPPHIRE = 'SA', _('Sapphire')

    title = models.CharField(
        max_length=TitleChoices.max_length(),
        choices=TitleChoices.choices,
    )

    image = models.URLField()

    colors = models.ManyToManyField(
        to=Color,
        through='StoneColor',
    )

    def __str__(self):
        return self.get_title_display()
