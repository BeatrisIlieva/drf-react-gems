from django.utils.translation import gettext_lazy as _
from django.db import models

from django_ts_gems.products.mixins import ChoicesMaxLengthMixin


class CategoryChoices(ChoicesMaxLengthMixin, models.TextChoices):
    BRACELET = 'BR', _('Bracelets')
    EARRING = 'EA', _('Earrings')
    NECKLACE = 'NE', _('Necklaces')
    RING = 'RI', _('Rings')


class CollectionChoices(ChoicesMaxLengthMixin, models.TextChoices):
    DAISY_DELIGHT = 'DA', _('Daisy Delight')
    ENGAGEMENT_WEDDING = 'EN', _('Engagement & Wedding')
    FORGET_ME_NOT = 'FO', _('Forget Me Not')
    LILY_BLOOM = 'LI', _('Lily Bloom')
    LOTUS_BLOSSOM = 'LO', _('Lotus Blossom')
    RADIANT_CLUSTER = 'RA', _('Radiant Cluster')
    SUNFLOWER = 'SU', _('Sunflower')


class ColorChoices(ChoicesMaxLengthMixin, models.TextChoices):
    BLUE = 'BL', _('Blue')
    GREEN = 'GR', _('Green')
    PINK = 'PI', _('Pink')
    RED = 'RE', _('Red')
    WHITE = 'WH', _('White')
    YELLOW = 'YE', _('Yellow')


class MaterialChoices(ChoicesMaxLengthMixin, models.TextChoices):
    YELLOW_GOLD = 'YE', _('Yellow Gold')
    ROSE_GOLD = 'RO', _('Rose Gold')
    PLATINUM = 'PL', _('Platinum')


class PrimaryStoneChoices(ChoicesMaxLengthMixin, models.TextChoices):
    AQUAMARINE = 'AQ', _('Aquamarine')
    BLUE_SAPPHIRE = 'BS', _('Blue Sapphire')
    EMERALD = 'EM', _('Emerald')
    PINK_SAPPHIRE = 'PS', _('Pink Sapphire')
    RUBY = 'RU', _('Ruby')
    WHITE_DIAMOND = 'WD', _('White Diamond')
    YELLOW_DIAMOND = 'YD', _('Yellow Diamond')
    YELLOW_SAPPHIRE = 'YS', _('Yellow Sapphire')


class StoneChoices(ChoicesMaxLengthMixin, models.TextChoices):
    AQUAMARINE = 'AQ', _('Aquamarine')
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


class ReferenceChoices(ChoicesMaxLengthMixin, models.TextChoices):
    FULL_MOTIF = 'FM', _('Full Motif')

