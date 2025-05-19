from django.db import models

from django.db.models import Min, Max, Sum, Case, Value, BooleanField, When
from itertools import groupby
from operator import itemgetter


class ProductManager(models.Manager):
    def get_products(self, category_id):
        qs = self.filter(category_id=category_id)
        raw_products = self._get_raw_products(qs)
        grouped_products = self._group_and_structure_products(raw_products)

        return grouped_products

    def _get_raw_products(self, qs):
        return (
            qs.select_related(
                'material',
                'collection',
                'category', 'reference'
            )

            .prefetch_related(
                'stone_by_color__color',
                'stone_by_color__stone'
            )
            .values(
                'id',
                'collection__name',
                'category__name',
                'reference__name',
                'material__name',
                'first_image',
                'second_image',
                'stone_by_color__color__name',
                'stone_by_color__stone__name',
                'stone_by_color__image',
                'stone_by_color__color__hex_code',
            )
            .annotate(
                min_price=Min('productvariant__price'),
                max_price=Max('productvariant__price'),
                total_quantity=Sum('productvariant__quantity'),
                is_sold_out=Case(
                    When(total_quantity=0, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
            .order_by('material__name', 'collection__name', 'category__name', 'reference__name')
        )

    def _group_and_structure_products(self, products):
        grouped = []

        for key, group in groupby(products, key=itemgetter(
                'collection__name', 'category__name', 'reference__name', 'material__name')):
            items = list(group)
            first = items[0]

            stones = self._extract_stones(items)
            stones = self._filter_white_diamonds_per_product(stones)

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
                'materials_count': stones[0]['materials_count'] if stones else 0,
                'total_quantity': first['total_quantity'],
                'is_sold_out': first['is_sold_out'],
            })

        return grouped

    def _extract_stones(self, items):
        stone_set = set()
        seen_products = set()

        for item in items:
            product_id = item['id']
            color = item['stone_by_color__color__name']
            name = item['stone_by_color__stone__name']
            image = item['stone_by_color__image']
            hex_code = item['stone_by_color__color__hex_code']

            if (color or name or image) and product_id and product_id:
                materials_count = self.filter(
                    collection__name=item['collection__name'],
                    category__name=item['category__name'],
                    reference__name=item['reference__name'],
                ).values('id').distinct('material__name').count()

                stone_set.add(
                    (
                        product_id,
                        color,
                        name,
                        image,
                        hex_code,
                        materials_count
                    )
                )

            seen_products.add(product_id)

        return [
            {
                'product_id': product_id,
                'color': color,
                'name': name,
                'image': image,
                'hex': hex_code,
                'materials_count': materials_count,
            }
            for (
                product_id,
                color,
                name,
                image,
                hex_code,
                materials_count
            ) in stone_set
        ]

    def _filter_white_diamonds_per_product(self, stones):
        from collections import defaultdict

        stones_by_product = defaultdict(list)
        for stone in stones:
            stones_by_product[stone['product_id']].append(stone)

        filtered_stones = []
        for product_id, product_stones in stones_by_product.items():
            only_white_diamond = all(
                s['name'] == 'Diamond' and s['color'] == 'White'
                for s in product_stones
            )
            if not only_white_diamond:
                product_stones = [
                    s for s in product_stones
                    if not (s['name'] == 'Diamond' and s['color'] == 'White')
                ]
            filtered_stones.extend(product_stones)

        return filtered_stones
