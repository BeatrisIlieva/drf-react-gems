from django.db import models

from django.db.models import (
    Sum,
    Case,
    Value,
    BooleanField,
    When,
    Count,
    CharField,
    IntegerField,
    Q,
    F
)
from itertools import groupby
from operator import itemgetter
from decimal import Decimal


class BaseProductManager(models.Manager):
    def get_product(self, item_id):
        return self.get(pk=item_id)

    def get_products(self, filters):
        qs = self.filter(filters)
        model_name = self.model.__name__.lower()

        raw_products = self._get_raw_products(qs, model_name)
        print(raw_products)
        grouped_products, colors_by_count, stones_by_count = self._group_and_structure_products(
            raw_products
        )
        materials_by_count = self._get_material_usage_count(raw_products)
        collections_by_count = self._get_collection_usage_count(raw_products)
        categories_by_count = self._get_categories_usage_count(raw_products)
        price_ranges = self._get_price_ranges(raw_products, model_name)

        return {
            'products': grouped_products,
            'colors_by_count': colors_by_count,
            'stones_by_count': stones_by_count,
            'materials_by_count': materials_by_count,
            'collections_by_count': collections_by_count,
            'categories_by_count': categories_by_count,
            'price_ranges': price_ranges,
        }

    def _get_raw_products(self, qs, model_name):
        return (
            qs.select_related(
                'material',
                'collection',
                'reference',
            )
            .prefetch_related(
                'stone_by_color__color',
                'stone_by_color__stone',
                'inventory'
            )
            .values(
                'id',
                'collection__name',
                'reference__name',
                'material__name',
                'material__id',
                'first_image',
                'second_image',
                'stone_by_color__color__name',
                'stone_by_color__color__id',
                'stone_by_color__stone__name',
                'stone_by_color__stone__id',
                'stone_by_color__image',
                'stone_by_color__color__hex_code',
            )
            .annotate(
                price=F('price'),
                total_quantity=Sum('inventory__quantity'),
                is_sold_out=Case(
                    When(total_quantity=0, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
            .order_by(
                'id',
                'material__name',
                'collection__name',
                'reference__name'
            )
        )

    def _group_and_structure_products(self, products):
        grouped = []
        colors_by_count = {}
        stones_by_count = {}

        for key, group in groupby(products, key=itemgetter(
                'collection__name',
                'reference__name',
                'material__name'
        )):
            items = list(group)
            first = items[0]

            stones = self._extract_stones(items)

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
                'reference__name': first['reference__name'],
                'first_image': first['first_image'],
                'second_image': first['second_image'],
                'stones': stones,
                'price': first['price'],
                'materials_count': materials,
                'total_quantity': first['total_quantity'],
                'is_sold_out': first['is_sold_out'],
            })

        grouped.sort(key=lambda item: len(item['stones']), reverse=True)

        return grouped, colors_by_count, stones_by_count

    def _extract_materials(self, items):
        for item in items:
            materials_count = self.filter(
                collection__name=item['collection__name'],
                reference__name=item['reference__name'],
            ).values('id').distinct('material__name').count()

        return materials_count

    def _extract_stones(self, items):
        products = []
        seen_products = set()

        for item in items:
            product_id = item['id']

            if (product_id in seen_products):
                continue

            color = item['stone_by_color__color__name']
            color_id = item['stone_by_color__color__id']
            stone = item['stone_by_color__stone__name']
            stone_id = item['stone_by_color__stone__id']
            image = item['stone_by_color__image']
            hex_code = item['stone_by_color__color__hex_code']

            products.append({
                'product_id': product_id,
                'color': color,
                'color_id': color_id,
                'stone': stone,
                'stone_id': stone_id,
                'image': image,
                'hex': hex_code,
            })

            seen_products.add(product_id)

        return products

    def _get_material_usage_count(self, qs):
        return (
            qs.values('material__name', 'material__id')
            .annotate(material_count=Count('id', distinct=True))
            .order_by('-material_count')
        )

    def _get_collection_usage_count(self, qs):
        return (
            qs.values('collection__name', 'collection__id')
            .annotate(collection_count=Count('id', distinct=True))
            .order_by('-collection_count')
        )

    def _get_categories_usage_count(self, qs):
        return (
            qs.values('reference__name', 'reference__id')
            .annotate(category_count=Count('id', distinct=True))
            .order_by('-category_count')
        )

    def _get_price_ranges(self, qs, model_name):

        return (
            qs
            .annotate(
                price_range=Case(
                    When(
                        Q(price__gte=Decimal(1000),
                          price__lt=Decimal(2999)),
                        then=Value('$1000 - $2999')
                    ),
                    When(
                        Q(price__gte=Decimal(3000),
                          price__lt=Decimal(5000)),
                        then=Value('$3000 - $4999')
                    ),
                    When(
                        Q(price__gte=Decimal(5000),
                          price__lt=Decimal(7000)),
                        then=Value('$5000 - $6999')
                    ),
                    When(
                        Q(price__gte=Decimal(7000),
                          price__lt=Decimal(9000)),
                        then=Value('$7000 - $8999')
                    ),
                    When(
                        Q(price__gte=Decimal(9000),
                          price__lt=Decimal(19999)),
                        then=Value('$9000 - $19999')
                    ),
                    default=Value('Unknown Price Range'),
                    output_field=CharField()
                )
            )
            .annotate(
                sort_order=Case(
                    When(price_range='$1000 - $2999', then=Value(1)),
                    When(price_range='$3000 - $4999', then=Value(2)),
                    When(price_range='$5000 - $6999', then=Value(3)),
                    When(price_range='$7000 - $8999', then=Value(4)),
                    When(price_range='$9000 - $19999', then=Value(5)),
                    default=Value(99),
                    output_field=IntegerField(),
                )
            )
            .values('price_range')
            .annotate(count=Count('id', distinct=True))
            .order_by('sort_order')
        )


class EarwearManager(BaseProductManager):
    pass


class FingerwearManager(BaseProductManager):
    pass


class NeckwearManager(BaseProductManager):
    pass


class WristwearManager(BaseProductManager):
    pass
