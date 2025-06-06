from django.db import models

from django.db.models import (
    Sum,
    Case,
    Value,
    BooleanField,
    When,
    Count,
    Min,
    Max,
    Avg
)


class ProductManager(models.Manager):
    def get_product_item(self, item_id):
        return self.get(pk=item_id)

    def get_product_list(self, filters, ordering):
        qs = self.filter(filters)

        raw_products = self._get_raw_products(qs, ordering)

        return raw_products

    def get_colors_by_count(self, raw_products):
        return self._get_entity_by_count(
            raw_products,
            'color',
            extra_fields=['hex_code']
        )

    def get_stones_by_count(self, raw_products):
        return self._get_entity_by_count(
            raw_products,
            'stone',
            extra_fields=['image']
        )

    def get_metals_by_count(self, raw_products):
        return self._get_entity_by_count(
            raw_products,
            'metal'
        )

    def get_collections_by_count(self, raw_products):
        return self._get_entity_by_count(
            raw_products,
            'collection'
        )

    def _get_raw_products(self, qs, ordering):
        ordering_map = {
            'price_asc': 'min',
            'price_desc': '-max',
            'rating': '-average_rating',
            'in_stock': '-inventory__quantity',
        }
        ordering_criteria = ordering_map[ordering]

        return (
            qs.select_related(
                'collection',
            )
            .prefetch_related(
                'inventory',
                'review'
            )
            .values(
                'id',
                'collection__name',
                'first_image',
                'second_image',
                'color__name',
                'stone__name',
                'metal__name',
            )
            .annotate(
                total_quantity=Sum('inventory__quantity'),
                min=Min('inventory__price'),
                max=Max('inventory__price'),
                is_sold_out=Case(
                    When(
                        total_quantity=0,
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                average_rating=Avg('review__rating', distinct=True),
            )
            .order_by(
                f'{ordering_criteria}',
                'id',
            )
        )

    def _get_entity_by_count(self, qs, entity, extra_fields=None):
        values_fields = [f'{entity}__name', f'{entity}__id']

        if extra_fields:
            values_fields.extend(
                [f'{entity}__{field}' for field in extra_fields])

        return (
            qs.values(
                *values_fields
            )
            .annotate(
                **{f'{entity}_count': Count('id', distinct=True)}
            )
            .order_by(
                f'-{entity}_count'
            )
        )
