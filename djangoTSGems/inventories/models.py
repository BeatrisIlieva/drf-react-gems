from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Inventory(models.Model):

    class Meta:
        unique_together = ('content_type', 'object_id', 'size')

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    size = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateField(
        auto_now_add=True,
    )
