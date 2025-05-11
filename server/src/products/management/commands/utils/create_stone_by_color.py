from src.products.models.characteristics.color import Color
from src.products.models.characteristics.stone import Stone
from src.products.models.characteristics.stone_by_color import StoneByColor


stone_by_color = {
    'Blue Aquamarine': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/aquamarine_b4dtyx.webp',
    'White Diamond': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748236/diamond_dkg8rb.webp',
    'Yellow Diamond': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745853383/brown-diamond-CD_xvzlf6.webp',
    'Green Emerald': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748237/emerald_auiwk4.webp',
    'Red Ruby': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/ruby_g7idgx.webp',
    'Blue Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748233/blue-sapphire_bjwmoo.webp',
    'Pink Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748232/pink-sapphire_se5pnk.webp',
    'Yellow Sapphire': 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745853383/yellow-sapphire_tukm7x.webp',
}


def create_stone_by_color():

    for key, value in stone_by_color.items():
        color_name, stone_name = key.split(' ')

        stone = Stone.objects.get(name=stone_name)
        color = Color.objects.get(name=color_name)

        StoneByColor.objects.get_or_create(
            image=value,
            color=color,
            stone=stone,
        )
