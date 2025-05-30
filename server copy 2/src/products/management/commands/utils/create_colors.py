from src.products.models import Color


colors = {
    'Blue': '#719cf0',
    'Green': '#06986f',
    'Pink': '#fa94ac',
    'Red': '#e93e3e',
    'White': '#fff',
    'Yellow': '#faf098',
}


def create_colors():
    for key, value in colors.items():
        Color.objects.create(
            name=key,
            hex_code=value,
        )
