from django.utils.translation import gettext_lazy as _
from django.db import models

from djangoTSGems.products.mixins import ChoicesMaxLengthMixin


class CategoryChoices(ChoicesMaxLengthMixin, models.TextChoices):
    BRACELET = 'BR', _('Bracelets')
    EARRING = 'EA', _('Earrings')
    NECKLACE = 'NE', _('Necklaces')
    RING = 'RI', _('Rings')


class CollectionChoices(ChoicesMaxLengthMixin, models.TextChoices):
    CLASSICS = 'CL', _('Classics')
    DAISY = 'DA', _('Daisy')
    FORGET_ME_NOT = 'FMN', _('Forget-Me-Not')
    LILY = 'LI', _('Lily')
    LOTUS = 'LO', _('Lotus')
    RADIANT = 'RA', _('Radiant')
    SUNFLOWER = 'SU', _('Sunflower')


class ColorChoices(ChoicesMaxLengthMixin, models.TextChoices):
    AQUAMARINE = 'AQ', _('Aquamarine')
    BLUE = 'BU', _('Blue')
    GREEN = 'GR', _('Green')
    PINK = 'PI', _('Pink')
    RED = 'RE', _('Red')
    WHITE = 'WH', _('White')
    YELLOW = 'YE', _('Yellow')


class MaterialChoices(ChoicesMaxLengthMixin, models.TextChoices):
    YELLOW_GOLD = 'YG', _('Yellow Gold')
    ROSE_GOLD = 'RG', _('Rose Gold')
    PLATINUM = 'ST', _('Platinum')


class StoneChoices(ChoicesMaxLengthMixin, models.TextChoices):
    DIAMOND = 'DI', _('Diamond')
    EMERALD = 'EM', _('Emerald')
    RUBY = 'RU', _('Ruby')
    SAPPHIRE = 'SA', _('Sapphire')


class SizeChoices(ChoicesMaxLengthMixin, models.TextChoices):
    XS = 'XS', _('XS')
    S = 'S', _('S')
    M = 'M', _('M')
    L = 'L', _('L')
    XL = 'XL', _('XL')
    ONE_SIZE = 'OS', _('OS')
