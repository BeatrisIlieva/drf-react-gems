from django.db import models


class CategoryChoices(models.TextChoices):
    BRACELET = 'BR', 'Bracelet'
    CHARM = 'CH', 'Charm'
    DROP_EARRING = 'DE', 'Drop Earring'
    NECKLACE = 'NE', 'Necklace'
    PENDANT = 'PE', 'Pendant'
    RING = 'RI', 'Ring'
    STUD_EARRING = 'SE', 'Stud Earring'


class ColorChoices(models.TextChoices):
    BLUE = 'BL', 'Blue'
    PINK = 'PI', 'Pink'
    WHITE = 'WH', 'White'
