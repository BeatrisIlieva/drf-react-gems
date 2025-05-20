from django.db import models

from django.db.models import Min, Max, Sum, Case, Value, BooleanField, When, F, Window
from django.db.models.functions import FirstValue
from itertools import groupby
from operator import itemgetter

from django.forms import ImageField


class ProductManager(models.Manager):
    def get_products(self, filters):
        qs = self.filter(filters)
        raw_products = self._get_raw_products(qs)
        # grouped_products, colors_by_count, stones_by_count = self._group_and_structure_products(
        #     raw_products)

        return raw_products
        # return {'products': grouped_products, 'colors_by_count': colors_by_count, 'stones_by_count': stones_by_count}

    def _get_raw_products(self, qs):
        return (
            qs.select_related(
                # 'material',
                'collection',
                'category',
                'reference'
            )
            .prefetch_related(
                'stone_by_color__color',
                'stone_by_color__stone'
            )
            .values(
                # 'id',
                'collection__name',
                'category__name',
                'reference__name',
                # 'material__name',
                # 'first_image',
                # 'second_image',
                # 'stone_by_color__color__name',
                # 'stone_by_color__color__id',
                # 'stone_by_color__stone__name',
                # 'stone_by_color__stone__id',
                # 'stone_by_color__image',
                # 'stone_by_color__color__hex_code',
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
            .order_by(
                # 'id',
                # 'material__name',
                'collection__name',
                'category__name',
                'reference__name'
            )            
        )

    def _group_and_structure_products(self, products):
        grouped = []
        colors_by_count = {}
        stones_by_count = {}
        # materials_by_count = {}

        for key, group in groupby(products, key=itemgetter(
                'collection__name',
                'category__name',
                'reference__name',
                'material__name'
        )):
            items = list(group)
            first = items[0]

            stones = self._extract_stones(items)
            stones = self._filter_white_diamonds_per_product(stones)
            materials = self._extract_materials(items)

            for stone in stones:
                if stone['color'] not in colors_by_count.keys():
                    colors_by_count[stone['color']] = {
                        'id': stone['color_id'],
                        'title': stone['color'],
                        'hex_code': stone['hex'],
                        'count': 0
                    }

                colors_by_count[stone['color']]['count'] += 1

                stone.pop('color_id')
                stone.pop('hex')

                if stone['stone'] not in stones_by_count.keys():
                    stones_by_count[stone['stone']] = {
                        'id': stone['stone_id'],
                        'title': stone['stone'],
                        'image': stone['image'],
                        'count': 0
                    }

                stones_by_count[stone['stone']]['count'] += 1

                stone.pop('stone_id')

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
                'materials_count': materials,
                'total_quantity': first['total_quantity'],
                'is_sold_out': first['is_sold_out'],
            })

        return grouped, colors_by_count, stones_by_count

    def _extract_materials(self, items):
        for item in items:
            materials_count = self.filter(
                collection__name=item['collection__name'],
                category__name=item['category__name'],
                reference__name=item['reference__name'],
            ).values('id').distinct('material__name').count()

        return materials_count

    def _extract_stones(self, items):
        stone_set = set()

        for item in items:
            product_id = item['id']
            color = item['stone_by_color__color__name']
            color_id = item['stone_by_color__color__id']
            stone = item['stone_by_color__stone__name']
            stone_id = item['stone_by_color__stone__id']
            image = item['stone_by_color__image']
            hex_code = item['stone_by_color__color__hex_code']

            if (color or stone or image) and product_id:
                stone_set.add(
                    (
                        product_id,
                        color,
                        color_id,
                        stone,
                        stone_id,
                        image,
                        hex_code,
                    )
                )

        return [
            {
                'product_id': product_id,
                'color': color,
                'color_id': color_id,
                'stone': stone,
                'stone_id': stone_id,
                'image': image,
                'hex': hex_code,
            }
            for (
                product_id,
                color,
                color_id,
                stone,
                stone_id,
                image,
                hex_code,
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
                s['stone'] == 'Diamond' and s['color'] == 'White'
                for s in product_stones
            )
            if not only_white_diamond:
                product_stones = [
                    s for s in product_stones
                    if not (s['stone'] == 'Diamond' and s['color'] == 'White')
                ]
            filtered_stones.extend(product_stones)

        return filtered_stones
