from django_ts_gems.products.models.product import Product
from django_ts_gems.products.models.relationships.category import Category
from django_ts_gems.products.models.relationships.collection import Collection
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.material import Material
from django_ts_gems.products.models.relationships.reference import Reference
from django_ts_gems.products.models.relationships.stone import Stone
from django_ts_gems.products.models.relationships.stones_colors import StonesColors


def create_product(product_data):

    category = Category.objects.get(
        category=product_data['category']
    )

    collection = Collection.objects.get(
        collection=product_data['collection']
    )

    reference = Reference.objects.get(
        reference=product_data['reference'],
    )

    material = Material.objects.get(
        name=product_data['material']
    )

    product = Product.objects.create(
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
