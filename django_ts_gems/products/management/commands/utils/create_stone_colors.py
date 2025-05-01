from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.stone import Stone
from django_ts_gems.products.models.relationships.stones_colors import StonesColors


stones_colors = {
    'Aquamarine Aquamarine': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/aquamarine_b4dtyx.webp',
    'White Diamond': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748236/diamond_dkg8rb.webp',
    'Yellow Diamond': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745853383/brown-diamond-CD_xvzlf6.webp',
    'Green Emerald': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748237/emerald_auiwk4.webp',
    'Red Ruby': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/ruby_g7idgx.webp',
    'Blue Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/blue-sapphire_bjwmoo.webp',
    'Pink Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/pink-sapphire_se5pnk.webp',
    'Yellow Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745853383/yellow-sapphire_tukm7x.webp',
}

for key, value in stones_colors.items():
    color_name, stone_name = key.split(' ')

    stone = Stone.objects.get(name=stone_name)
    color = Color.objects.get(name=color_name)

    StonesColors.objects.get_or_create(
        image=value,
        color=color,
        stone=stone,
    )
