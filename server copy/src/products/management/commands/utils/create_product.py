import random

from src.products.models.relationships.size import Size
from src.products.models.product_item import ProductItem
from src.products.models.product_variant import ProductVariant
from src.products.models.relationships.category import Category
from src.products.models.relationships.collection import Collection
from src.products.models.relationships.color import Color
from src.products.models.relationships.material import Material
from src.products.models.relationships.reference import Reference
from src.products.models.relationships.stone import Stone
from src.products.models.relationships.stone_by_color import StoneByColor


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
    first_image = product_data['first_image']
    second_image = product_data['second_image']
    
    stone = product_data['stone_by_color']

    color_name, stone_name = stone.split(' ')

    color = Color.objects.get(name=color_name)
    stone = Stone.objects.get(name=stone_name)

    stone_by_color = StoneByColor.objects.get(
        color=color,
        stone=stone,
    )

    product_item = ProductItem.objects.create(
        first_image=first_image,
        second_image=second_image,
        category=category,
        collection=collection,
        reference=reference,
        material=material,
        stone_by_color=stone_by_color
    )



    price = product_data['price']
    one_size = Size.objects.filter(name='One Size')
    all_sizes = Size.objects.exclude(name='One Size')

    if category.name == 'Earwear':
        size_list = one_size
    else:
        size_list = all_sizes

    current_price = price
    for size in size_list:
        quantity = random.randint(2, 5)

        ProductVariant.objects.create(
            size=size,
            price=current_price,
            quantity=quantity,
            product_item=product_item
        )

        current_price += 180
