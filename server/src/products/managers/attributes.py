from django.db import models
from django.db.models import Count


class BaseAttributesManager(models.Manager):
    def get_attributes_count(self, filters, category):
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


class ColorManager(BaseAttributesManager):
    pass


class CollectionManager(BaseAttributesManager):
    pass


class MetalManager(BaseAttributesManager):
    pass


class StoneManager(BaseAttributesManager):
    pass
