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
    Min,
    Max,
)

from decimal import Decimal


class ProductManager(models.Manager):
    def get_product_item(self, item_id):
        return self.get(pk=item_id)

    def get_product_list(self, filters):
        qs = self.filter(filters)

        raw_products = self._get_raw_products(qs)

        return raw_products

    def get_colors_by_count(self, raw_products):
        return self._get_entity_by_count(raw_products, 'color', extra_fields=['hex_code'])

    def get_stones_by_count(self, raw_products):
        return self._get_entity_by_count(raw_products, 'stone', extra_fields=['image'])

    def get_metals_by_count(self, raw_products):
        return self._get_entity_by_count(raw_products, 'metal')

    def get_collections_by_count(self, raw_products):
        return self._get_entity_by_count(raw_products, 'collection')

    def get_price_ranges_by_count(self, raw_products):
        return (
            raw_products
            .annotate(
                price_range=Case(
                    When(
                        Q(inventory__price__gte=Decimal(1000),
                          inventory__price__lt=Decimal(2999)),
                        then=Value('$1000 - $2999')
                    ),
                    When(
                        Q(inventory__price__gte=Decimal(3000),
                          inventory__price__lt=Decimal(5000)),
                        then=Value('$3000 - $4999')
                    ),
                    When(
                        Q(inventory__price__gte=Decimal(5000),
                          inventory__price__lt=Decimal(7000)),
                        then=Value('$5000 - $6999')
                    ),
                    When(
                        Q(inventory__price__gte=Decimal(7000),
                          inventory__price__lt=Decimal(9000)),
                        then=Value('$7000 - $8999')
                    ),
                    When(
                        Q(inventory__price__gte=Decimal(9000),
                          inventory__price__lt=Decimal(19999)),
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

    def _get_raw_products(self, qs):
        return (
            qs.select_related(
                'collection',
            )
            .prefetch_related(
                'inventory',
            )
            .values(
                'id',
                'collection__name',
                'first_image',
                'second_image',
                'color__name',
                'stone__name',
                'metal__name'
            )
            .annotate(
                total_quantity=Sum('inventory__quantity'),
                min=Min('inventory__price'),
                max=Max('inventory__price'),
                is_sold_out=Case(
                    When(total_quantity=0, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
            .order_by(
                'id',
                'collection__name',
            )
        )

    def _get_entity_by_count(self, qs, entity, extra_fields=None):
        values_fields = [f'{entity}__name', f'{entity}__id']
        if extra_fields:
            values_fields.extend(
                [f'{entity}__{field}' for field in extra_fields])
        return (
            qs.values(*values_fields)
            .annotate(**{f'{entity}_count': Count('id', distinct=True)})
            .order_by(f'-{entity}_count')
        )
