from django.db import models
from django.db.models import Q
from typing import Dict
from src.products.constants import NameFieldLengths


class NameFieldMixin(models.Model):
    NAME_MAX_LENGTH: int = NameFieldLengths.NAME_MAX_LENGTH

    class Meta:
        abstract = True

    name: models.CharField = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,

    )

    def __str__(self) -> str:
        return self.name


class FilterMixin:
    def _get_params(self) -> Dict[str, list[str]]:
        return {
            'colors': self.request.query_params.getlist('colors'),
            'stones': self.request.query_params.getlist('stones'),
            'metals': self.request.query_params.getlist('metals'),
            'collections': self.request.query_params.getlist('collections'),
        }

    def _get_filters_for_attributes(self, category: str) -> Q:
        params: Dict[str, list[str]] = self._get_params()
        filters: Q = Q()

        if params['colors']:
            filters &= Q(**{f'{category}__color_id__in': params['colors']})
        if params['stones']:
            filters &= Q(**{f'{category}__stone_id__in': params['stones']})
        if params['metals']:
            filters &= Q(**{f'{category}__metal_id__in': params['metals']})
        if params['collections']:
            filters &= Q(
                **{f'{category}__collection_id__in': params['collections']})

        return filters

    def _get_filters_for_product(self) -> Q:
        params: Dict[str, list[str]] = self._get_params()
        filters: Q = Q()

        if params['colors']:
            filters &= Q(color_id__in=params['colors'])
        if params['stones']:
            filters &= Q(stone_id__in=params['stones'])
        if params['metals']:
            filters &= Q(metal__id__in=params['metals'])
        if params['collections']:
            filters &= Q(collection__id__in=params['collections'])

        return filters
