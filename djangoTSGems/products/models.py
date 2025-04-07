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

    def __str__(self):
        gemstone_display = dict(self.GEMSTONE_CHOICES).get(
            self.gemstone, self.gemstone)
        return f"{gemstone_display} {self.__class__.__name__}"


class DropEarring(Product):
    pass


class StudEarring(Product):
    pass


class Charm(Product):
    pass


class Necklace(Product):
    pass


class Pendant(Product):
    pass


class Bracelet(Product):
    pass


class Ring(Product):
    pass
