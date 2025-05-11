from django.db import models


class StoneByColor(models.Model):


    image = models.URLField()

    color = models.ForeignKey(
        to='products.Color',
        on_delete=models.CASCADE,
    )

    stone = models.ForeignKey(
        to='products.Stone',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f'{self.color.name} {self.stone.name}'
