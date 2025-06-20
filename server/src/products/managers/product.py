from django.db import models

from django.db.models import (
    Sum,
    Case,
    Value,
    BooleanField,
    When,
    Min,
    Max,
    Avg
)


class BaseProductManager(models.Manager):
    def get_product_item(self, item_id):
        return self.get(pk=item_id)

    def get_product_list(self, filters, ordering):
        qs = self.filter(filters)

        raw_products = self._get_raw_products(qs, ordering)

        return raw_products

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


class EarwearManager(BaseProductManager):
    pass


class NeckwearManager(BaseProductManager):
    pass


class WristwearManager(BaseProductManager):
    pass


class FingerwearManager(BaseProductManager):
    pass
