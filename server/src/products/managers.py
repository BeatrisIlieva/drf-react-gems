from django.db import models

from django.db.models import Min, Max
from itertools import groupby
from operator import itemgetter


class ProductManager(models.Manager):
    def get_products(self, category_id):
        qs = self.filter(category_id=category_id)

        products = (
            qs
            .select_related('material', 'collection', 'category', 'reference')
            .prefetch_related('stone_by_color__color', 'stone_by_color__stone')
            .values(
                'id',
                'collection__name',
                'category__name',
                'reference__name',
                'first_image',
                'second_image',
                'stone_by_color__color__name',
                'stone_by_color__stone__name',
                'stone_by_color__image',
                'stone_by_color__color__hex_code',
                'material__name'
            )
            .annotate(
                min_price=Min('productvariant__price'),
                max_price=Max('productvariant__price'),
            )
            .order_by('collection__name', 'category__name', 'reference__name', 'material__name')
        )

        grouped = []

        for key, group in groupby(products, key=itemgetter('collection__name', 'category__name', 'reference__name', 'material__name')):
            items = list(group)
            first = items[0]

            stone_set = set()

            seen_products = []

            for item in items:
                product_id = item['id']
                color = item['stone_by_color__color__name']
                name = item['stone_by_color__stone__name']
                image = item['stone_by_color__image']
                hex_code = item['stone_by_color__color__hex_code']

                if (color or name or image) and product_id not in seen_products:

                    stone_set.add((product_id, color, name, image, hex_code))

                seen_products.append(product_id)

            stones = [
                {'product_id': product_id, 'color': color,
                    'name': name, 'image': image, 'hex': hex_code}
                for (product_id, color, name, image, hex_code) in stone_set
            ]

            grouped.append({
                'id': first['id'],
                'collection__name': first['collection__name'],
                'category__name': first['category__name'],
                'reference__name': first['reference__name'],
                'first_image': first['first_image'],
                'second_image': first['second_image'],
                'stones': stones,
                'min_price': first['min_price'],
                'max_price': first['max_price'],
            })

        return grouped
