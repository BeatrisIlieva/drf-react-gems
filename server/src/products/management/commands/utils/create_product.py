import random
from django.contrib.contenttypes.models import ContentType

from src.products.models import (
    Collection,
    Color,
    Metal,
    Stone,
    Size,
    Inventory,
)
from src.products.models.product import Bracelet, Earring, Necklace, Pendant, Ring, Watch

categories_mapper = {
    'Earring': Earring,
    'Necklace': Necklace,
    'Pendant': Pendant,
    'Bracelet': Bracelet,
    'Watch': Watch,
    'Ring': Ring,
}


def create_product(product_data):

    collection = Collection.objects.get(name=product_data['collection'])

    metal = Metal.objects.get(name=product_data['material'])

    first_image = product_data['first_image']
    second_image = product_data['second_image']
    third_image = product_data['third_image']
    fourth_image = product_data['fourth_image']

    description = product_data['description']
    target_gender = product_data['target_gender']

    stone = product_data['stone_by_color']
    color_name, stone_name = stone.split(' ')

    color = Color.objects.get(name=color_name)
    stone = Stone.objects.get(name=stone_name)

    price = product_data['price']
    current_price = price + random.randint(2, 17)

    model_class = categories_mapper[product_data['category']]

    product = model_class.objects.create(
        first_image=first_image,
        second_image=second_image,
        third_image=third_image,
        fourth_image=fourth_image,
        collection=collection,
        metal=metal,
        color=color,
        stone=stone,
        description=description,
        target_gender=target_gender,
    )

    sizes = Size.objects.all()
    product_ct = ContentType.objects.get_for_model(model_class)

    for size in sizes:

        Inventory.objects.create(
            size=size,
            price=current_price,
            content_type=product_ct,
            object_id=product.id,
        )

        current_price = current_price + (100 + random.randint(4, 17))
