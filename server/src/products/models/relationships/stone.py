from django.db import models

from src.products.mixins import NameFieldMixin


class Stone(NameFieldMixin, models.Model):

    image = models.URLField()
