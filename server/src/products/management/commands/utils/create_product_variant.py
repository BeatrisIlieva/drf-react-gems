import random
from src.products.models import ProductVariant
from src.products.models.characteristics.size import Size


def create_product_variant(product, price):
    sizes = Size.objects.all()
    one_size = sizes.get(size='One Size')
    quantity = random.randint(2, 5)
    category = product.category

    category_mapping = {
        'Earring': [one_size],
    }

    default_sizes = sizes

    size_list = category_mapping.get(category, default_sizes)

    create_product_variant_object(product, size_list, price, quantity)


def create_product_variant_object(product, sizes, price, quantity):

    for size in sizes:
        ProductVariant.objects.create(
            product_item=product,
            size=size,
            price=price,
            quantity=quantity,
        )
