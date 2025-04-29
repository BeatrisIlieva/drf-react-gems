
from django.db import models

from django_ts_gems.products.choices import PrimaryStoneChoices


class PrimaryStone(models.Model):

    primary_stone = models.CharField(
        max_length=PrimaryStoneChoices.max_length(),
        choices=PrimaryStoneChoices.choices,
        unique=True,
        error_messages={
            'unique': 'This primary stone already exists.'
        }
    )

    image = models.URLField()
    
    
    def __str__(self):
        return self.get_primary_stone_display()
