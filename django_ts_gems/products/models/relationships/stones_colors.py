from django.db import models


class StonesColors(models.Model):

    image = models.URLField()

    color = models.ForeignKey(
        to='Color',
        on_delete=models.CASCADE,
    )

    stone = models.ForeignKey(
        to='Stone',
        on_delete=models.CASCADE,
    )
