import random

from src.products.models.earwear import Earwear, EarwearInventory
from src.products.models.fingerwear import Fingerwear, FingerwearSize, FingerwearInventory
from src.products.models.neckwear import Neckwear, NeckwearSize, NeckwearInventory
from src.products.models.wristwear import Wristwear, WristwearSize, WristwearInventory
from src.products.models.relationships.collection import Collection
from src.products.models.relationships.color import Color
from src.products.models.relationships.material import Material
from src.products.models.relationships.reference import Reference
from src.products.models.relationships.stone import Stone
from src.products.models.relationships.stone_by_color import StoneByColor


categories_mapper = {
    'Earwear': Earwear,
    'Fingerwear': Fingerwear,
    'Neckwear': Neckwear,
    'Wristwear': Wristwear,
}

sizes_mapper = {
    'Fingerwear': FingerwearSize,
    'Neckwear': NeckwearSize,
    'Wristwear': WristwearSize,
}

inventories_mapper = {
    'Fingerwear': FingerwearInventory,
    'Neckwear': NeckwearInventory,
    'Wristwear': WristwearInventory,
    'Earwear': EarwearInventory,
}


def create_product(product_data):
    collection = Collection.objects.get(
        name=product_data['collection']
    )
    reference = Reference.objects.get(
        name=product_data['reference'],
    )
    material = Material.objects.get(
        name=product_data['material']
    )
    category = product_data['category']
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

    modelName = categories_mapper[category]
    price = product_data['price']
    current_price = price + random.randint(2, 17)
    inventory = inventories_mapper[category]

    product = modelName.objects.create(
        first_image=first_image,
        second_image=second_image,
        collection=collection,
        reference=reference,
        material=material,
        stone_by_color=stone_by_color,
    )

    if category == 'Earwear':
        quantity = random.randint(0, 6)

        inventory.objects.create(
            price=current_price,
            quantity=quantity,
            product=product,
        )

    else:
        sizes = sizes_mapper[category].objects.all()

        for size in sizes:
            quantity = random.randint(0, 6)
            inventory.objects.create(
                size=size,
                price=current_price,
                quantity=quantity,
                product=product
            )

            current_price += (180 + random.randint(11, 56))
