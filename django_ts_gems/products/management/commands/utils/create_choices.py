from django_ts_gems.products.models.relationships.category import Category
from django_ts_gems.products.models.relationships.collection import Collection
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.material import Material
from django_ts_gems.products.models.relationships.primary_stone import PrimaryStone
from django_ts_gems.products.models.relationships.reference import Reference
from django_ts_gems.products.models.relationships.stone import Stone
from django_ts_gems.products.models.size import Size


from django_ts_gems.products.choices import (
    CategoryChoices,
    CollectionChoices,
    ColorChoices,
    MaterialChoices,
    PrimaryStoneChoices,
    ReferenceChoices,
    SizeChoices,
    StoneChoices
)

from django_ts_gems.products.management.data import (
    stones,
    primary_stones,
    colors,
)


def create_choices():
    for choice in CategoryChoices:
        Category.objects.get_or_create(
            category=choice.value,
        )

    for choice in CollectionChoices:
        Collection.objects.get_or_create(
            collection=choice.value,
        )

    for choice in ColorChoices:
        Color.objects.get_or_create(
            color=choice.value,
            hex_code=colors[choice.value]
        )

    for choice in MaterialChoices:
        Material.objects.get_or_create(
            material=choice.value,
        )

    for choice in PrimaryStoneChoices:
        PrimaryStone.objects.get_or_create(
            primary_stone=choice.value,
            image=primary_stones[choice.value],
        )

    for choice in ReferenceChoices:
        Reference.objects.get_or_create(
            reference=choice.value,
        )

    for choice in StoneChoices:
        Stone.objects.get_or_create(
            stone=choice.value,
            image=stones[choice.value],
        )

    for choice in SizeChoices:
        Size.objects.get_or_create(
            size=choice.value,
        )
