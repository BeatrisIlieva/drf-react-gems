from django.db import models

from django_ts_gems.products.mixins import ChoicesMaxLengthMixin


class CategoryChoices(ChoicesMaxLengthMixin, models.TextChoices):
    BRACELET = 'Bracelet', 'Bracelet'
    EARRING = 'Earring', 'Earring'
    NECKLACE = 'Necklace', 'Necklace'
    RING = 'Ring', 'Ring'


class CollectionChoices(ChoicesMaxLengthMixin, models.TextChoices):
    DAISY = 'Daisy', 'Daisy'
    GERBERA = 'Gerbera', 'Gerbera'
    FORGET_ME_NOT = 'Forget Me Not', 'Forget Me Not'
    LILY = 'Lily', 'Lily'
    LOTUS = 'Lotus', 'Lotus'
    BERRY = 'Berry', 'Berry'
    SUNFLOWER = 'Sunflower', 'Sunflower'
    LILY_OF_THE_VALLEY = 'Lily of the Valley', 'Lily of the Valley'


class ColorChoices(ChoicesMaxLengthMixin, models.TextChoices):
    BLUE = 'Blue', 'Blue'
    GREEN = 'Green', 'Green'
    PINK = 'Pink', 'Pink'
    RED = 'Red', 'Red'
    WHITE = 'White', 'White'
    YELLOW = 'Yellow', 'Yellow'


class MaterialChoices(ChoicesMaxLengthMixin, models.TextChoices):
    YELLOW_GOLD = 'Yellow Gold', 'Yellow Gold'
    ROSE_GOLD = 'Rose Gold', 'Rose Gold'
    PLATINUM = 'Platinum', 'Platinum'


class StoneChoices(ChoicesMaxLengthMixin, models.TextChoices):
    AQUAMARINE = 'Aquamarine', 'Aquamarine'
    DIAMOND = 'Diamond', 'Diamond'
    EMERALD = 'Emerald', 'Emerald'
    RUBY = 'Ruby', 'Ruby'
    SAPPHIRE = 'Sapphire', 'Sapphire'


class SizeChoices(ChoicesMaxLengthMixin, models.TextChoices):
    XS = 'XS', 'XS'
    S = 'S', 'S'
    M = 'M', 'M'
    L = 'L', 'L'
    XL = 'XL', 'XL'
    ONE_SIZE = 'One Size', 'One Size'


class ReferenceChoices(ChoicesMaxLengthMixin, models.TextChoices):
    STUD = 'Stud', 'Stud'
    DROP = 'Drop', 'Drop'
    PENDANT = 'Pendant', 'Pendant'
    LARIAT = 'Lariat', 'Lariat'
    TENNIS = 'Tennis', 'Tennis'
    CHAIN = 'Chain', 'Chain'
    STATEMENT = 'Statement', 'Statement'
    BAND = 'Band', 'Band'
