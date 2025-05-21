from django.db import models

from src.products.mixins import CaseInsensitiveUniqueNameFieldMixin, NameFieldMixin


class Stone(NameFieldMixin, CaseInsensitiveUniqueNameFieldMixin, models.Model):

    image = models.URLField()
