from django_ts_gems.products.models.relationships.category import Category
from django_ts_gems.products.models.relationships.collection import Collection
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.material import Material
from django_ts_gems.products.models.relationships.reference import Reference
from django_ts_gems.products.models.relationships.stone import Stone
from django_ts_gems.products.models.size import Size


from django_ts_gems.products.choices import (
    CategoryChoices,
    CollectionChoices,
    ColorChoices,
    MaterialChoices,
    ReferenceChoices,
    SizeChoices,
    StoneChoices
)


stones = {
    'Aquamarine': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/aquamarine_b4dtyx.webp',
    'Diamond': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748236/diamond_dkg8rb.webp',
    'Emerald': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748237/emerald_auiwk4.webp',
    'Ruby': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/ruby_g7idgx.webp',
    'Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/blue-sapphire_bjwmoo.webp',
}

colors = {
    'Blue': '#719cf0',
    'Green': '#06986f',
    'Pink': '#fa94ac',
    'Red': '#e93e3e',
    'White': '#fff',
    'Yellow': '#faf098',
}


def create_choices():
    for choice in CategoryChoices:
        Category.objects.get_or_create(
            name=choice.value,
        )

    for choice in CollectionChoices:
        Collection.objects.get_or_create(
            name=choice.value,
        )

    for choice in ColorChoices:
        Color.objects.get_or_create(
            name=choice.value,
            hex_code=colors[choice.value]
        )

    for choice in MaterialChoices:
        Material.objects.get_or_create(
            name=choice.value,
        )

    for choice in ReferenceChoices:
        Reference.objects.get_or_create(
            name=choice.value,
        )

    for choice in StoneChoices:
        Stone.objects.get_or_create(
            name=choice.value,
            image=stones[choice.value],
        )

    for choice in SizeChoices:
        Size.objects.get_or_create(
            size=choice.value,
        )
