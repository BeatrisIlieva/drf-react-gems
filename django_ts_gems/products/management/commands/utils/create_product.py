from django_ts_gems.products.models.product import Product
from django_ts_gems.products.models.relationships.category import Category
from django_ts_gems.products.models.relationships.collection import Collection
from django_ts_gems.products.models.relationships.color import Color
from django_ts_gems.products.models.relationships.description import Description
from django_ts_gems.products.models.relationships.material import Material
from django_ts_gems.products.models.relationships.media import Media
from django_ts_gems.products.models.relationships.primary_stone import PrimaryStone
from django_ts_gems.products.models.relationships.reference import Reference
from django_ts_gems.products.models.relationships.stone import Stone


def create_product(product_data):

    category = Category.objects.get(
        category=product_data['category']
    )

    collection = Collection.objects.get(
        collection=product_data['collection']
    )

    primary_stone = PrimaryStone.objects.get(
        primary_stone=product_data['primary_stone']
    )

    reference = Reference.objects.get(
        reference=product_data['reference'],
    )

    description = Description.objects.create(
        description=product_data['description']
    )

    product = Product.objects.create(
        category=category,
        collection=collection,
        description=description,
        primary_stone=primary_stone,
        reference=reference,
    )

    product.colors.set(
        Color.objects.filter(
            color__in=product_data['colors']
        ))

    product.materials.set(Material.objects.filter(
        material__in=product_data['materials']
    ))

    product.stones.set(Stone.objects.filter(
        stone__in=product_data['stones']
    ))

    media = Media.objects.create(
        first_image=product_data['first_image'],
        second_image=product_data['second_image'],
        third_image=product_data['third_image'],
        fourth_image=product_data['fourth_image'],
    )

    product.media = media
    product.save()

    return product
