from typing import Any
from django.db import models
from django.db.models import (
    Sum,
    Case,
    Value,
    BooleanField,
    When,
    Min,
    Max,
    Avg,
    Count
)


class BaseProductManager(models.Manager):
    def get_product_item(
        self,
        item_id: int
    ) -> Any:
        return self.get(pk=item_id)

    def get_product_list(
        self,
        filters: dict[str, Any],
        ordering: str
    ) -> Any:
        qs = self.filter(filters)
        raw_products = self._get_raw_products(qs, ordering)
        return raw_products

    def _get_raw_products(
        self,
        qs: Any,
        ordering: str
    ) -> Any:
        ordering_map = {
            'price_asc': 'min_price',
            'price_desc': '-max_price',
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
                min_price=Min('inventory__price'),
                max_price=Max('inventory__price'),
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


class BaseAttributesManager(models.Manager):
    def get_attributes_count(
        self,
        filters: dict[str, Any],
        category: str
    ) -> Any:
        qs = self.get_queryset()
        return (
            qs
            .prefetch_related(
                category
            )
            .filter(
                filters,
            )
            .values(
                'id',
                'name'
            )
            .annotate(
                count=Count(
                    category,
                )
            )
            .filter(count__gt=0)
        )
