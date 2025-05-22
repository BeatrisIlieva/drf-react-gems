from django.core.exceptions import ValidationError
from django.db import models


class NameFieldMixin(models.Model):
    NAME_MAX_LENGTH = 30

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,

    )

    def __str__(self):
        return self.name


class CaseInsensitiveUniqueNameFieldMixin:
    def clean(self):
        model = self.__class__

        if model.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError({
                'name': f'A {model.__name__.lower()} with this name already exists (case-insensitive).'
            })


class InventoryInfoMixin:
    def __str__(self):
        return f'Price: {self.inventory.price} - Quantity: {self.inventory.quantity} - Size: {self.inventory.size.name} cm.'
