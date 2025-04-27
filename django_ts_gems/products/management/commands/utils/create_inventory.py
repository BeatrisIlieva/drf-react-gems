import random
from django_ts_gems.inventories.models import Inventory
from django_ts_gems.products.models.size import Size


def create_inventory(product):
    sizes = Size.objects.all()
    one_size = sizes.get(size='OS')
    quantity = random.randint(2, 5)
    category = product.category.get_title_display()  
    price = product.price

    category_mapping = {
        'Earrings': [one_size],
    }

    default_sizes = sizes

    size_list = category_mapping.get(category, default_sizes)

    create_inventory_object(product, size_list, price, quantity)


def create_inventory_object(product, sizes, price, quantity):

    for size in sizes:
        Inventory.objects.create(
            product=product,
            size=size,
            price=price,
            quantity=quantity,
        )
