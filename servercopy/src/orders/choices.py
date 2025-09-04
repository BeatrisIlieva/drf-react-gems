from django.db import models

from src.common.utils import ChoicesMaxLengthMixin


class OrderStatusChoices(ChoicesMaxLengthMixin, models.TextChoices):
    PENDING = 'PE', 'Pending'
    COMPLETED = 'CO', 'Completed'
