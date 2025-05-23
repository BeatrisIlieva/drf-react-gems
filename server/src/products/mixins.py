from django.db import models


class NameFieldMixin(models.Model):
    NAME_MAX_LENGTH = 30

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,

    )

    def __str__(self):
        return self.name


class InventoryInfoMixin:
    def __str__(self):
        return f'Price: {self.price} - Quantity: {self.quantity} - Size: {self.size.name} cm.'
