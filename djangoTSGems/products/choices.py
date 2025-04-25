from django.db import models


class BraceletTypeChoices(models.TextChoices):
    CHAIN = 'CH', 'Chain'
    BEAD = 'BE', 'Bead'
    BANGLE = 'BA', 'Bangle'
    CUFF = 'CU', 'Cuff'


class EarringTypeChoices(models.TextChoices):
    DROP = 'DR', 'Drop'
    STUD = 'ST', 'Stud'
    HOOP = 'HO', 'Hoop'
    CHANDELIER = 'CH', 'Chandelier'


class RingTypeChoices(models.TextChoices):
    BAND = 'BA', 'Band'
    PETITE = 'PE', 'Petite'
    PINKY = 'PI', 'Pinky'
    STATEMENT = 'ST', 'Statement'
