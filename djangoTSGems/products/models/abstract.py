from django.db import models


class Product(models.Model):
    class Meta:
        abstract = True

    GEMSTONE_CHOICES = (
        ("PS", "Pink Sapphire"),
        ("BS", "Blue Sapphire"),
        ("BD", "Brilliant Diamond"),
    )

    gemstone = models.CharField(
        max_length=2,
        choices=GEMSTONE_CHOICES,
    )

    first_image_url = models.URLField()

    second_image_url = models.URLField()

    description = models.TextField(
        max_length=300,
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        gemstone_display = dict(self.GEMSTONE_CHOICES).get(self.gemstone, self.gemstone)
        return f"{gemstone_display} {self.__class__.__name__}"


class FlexibleSizeProduct(Product):
    class Meta:
        abstract = True

    SIZE_CHOICES = ()

    size = models.CharField(max_length=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('size').choices = self.SIZE_CHOICES


class FixedSizeProduct(Product):
    class Meta:
        abstract = True

    size = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
