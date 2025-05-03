from src.products.models.product_item import ProductItem
from src.products.models.characteristics.category import Category
from src.products.models.characteristics.collection import Collection
from src.products.models.characteristics.color import Color
from src.products.models.characteristics.material import Material
from src.products.models.characteristics.reference import Reference
from src.products.models.characteristics.stone import Stone
from src.products.models.characteristics.stones_colors import StonesColors


def create_product_item(product_data):

    category = Category.objects.get(
        name=product_data['category']
    )

    collection = Collection.objects.get(
        name=product_data['collection']
    )

    reference = Reference.objects.get(
        name=product_data['reference'],
    )

    material = Material.objects.get(
        name=product_data['material']
    )

    product = ProductItem.objects.create(
        first_image=product_data['first_image'],
        second_image=product_data['second_image'],
        category=category,
        collection=collection,
        reference=reference,
        material=material,
    )

    for element in product_data['stones_colors']:
        color_name, stone_name = element.split(' ')

        color = Color.objects.get(name=color_name)
        stone = Stone.objects.get(name=stone_name)

        stone_color = StonesColors.objects.get(
            color=color,
            stone=stone,
        )

        product.stones_colors.add(stone_color)

    return product
