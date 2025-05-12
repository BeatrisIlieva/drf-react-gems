import random

from src.products.models.relationships.size import Size
from src.products.models.product import Product
from src.products.models.relationships.category import Category
from src.products.models.relationships.collection import Collection
from src.products.models.relationships.color import Color
from src.products.models.relationships.material import Material
from src.products.models.relationships.reference import Reference
from src.products.models.relationships.stone import Stone
from src.products.models.relationships.stone_by_color import StoneByColor

from src.products.management.commands.utils.create_media import create_media


def create_product(product_data):

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

    first_image_url = product_data['first_image']
    second_image_url = product_data['second_image']
    first_image = create_media(first_image_url, 'first_image')
    second_image = create_media(second_image_url, 'second_image')

    price = product_data['price']

    quantity = random.randint(2, 5)
    
    one_size = Size.objects.filter(name='One Size')

    all_sizes = Size.objects.exclude(name='One Size')
    
    if category.name == 'Earwear':
        size_list = one_size
    else:
        size_list = all_sizes

    stones = product_data['stone_by_color']

    current_price = price

    for size in size_list:

        product = Product.objects.create(
            size=size,
            price=current_price,
            quantity=quantity,
            first_image=first_image,
            second_image=second_image,
            category=category,
            collection=collection,
            reference=reference,
            material=material
        )

        current_price += 180

        for element in stones:
            color_name, stone_name = element.split(' ')

            color = Color.objects.get(name=color_name)
            stone = Stone.objects.get(name=stone_name)

            stone_color = StoneByColor.objects.get(
                color=color,
                stone=stone,
            )

            product.stone_by_color.add(stone_color)
