from django.db import models
from django.db.models import Q
from src.products.constants import NameFieldLengths


class NameFieldMixin(models.Model):
    """
    Mixin class that provides a standardized name field for various entities.

    This mixin is used by entities like Collection, Color, Metal, Stone, and Size
    to ensure they all have a consistent name field with the same constraints.
    Using a mixin instead of repeating the field definition in each model
    promotes DRY (Don't Repeat Yourself) principles and makes maintenance easier.

    The mixin uses the NAME_MAX_LENGTH constant from the constants module,
    ensuring consistency across the application.
    """

    NAME_MAX_LENGTH = NameFieldLengths.NAME_MAX_LENGTH

    class Meta:
        abstract = True

    # Standardized name field used across multiple entities
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )

    def __str__(self):
        return self.name


class FilterMixin:
    """
    Mixin class that provides filtering functionality for product listings.

    This mixin is used by views that need to filter products based on
    various attributes like colors, stones, metals, and collections.
    It provides methods to extract filter parameters from request query
    strings and build database queries.

    The mixin supports both filtering by product attributes directly
    and filtering by related inventory attributes.
    """

    def _get_params(self):
        """
        Extract filter parameters from the request query string.

        This method looks for specific query parameters in the request
        and returns them as a dictionary. The parameters are expected
        to be lists (multiple values can be selected for each filter).
        """
        return {
            'colors': self.request.query_params.getlist('colors'),
            'stones': self.request.query_params.getlist('stones'),
            'metals': self.request.query_params.getlist('metals'),
            'collections': self.request.query_params.getlist('collections'),
        }

    def _build_filters(self, params, filter_map):
        """
        Build database filters based on provided parameters and filter mapping.
        """
        filters = Q()

        for key, value in params.items():
            if value and key in filter_map:
                filters &= Q(**{filter_map[key]: value})

        return filters

    def _get_filters_for_attributes(self, category):
        """
        Build database filters for attribute-based filtering.
        """
        params = self._get_params()

        filter_map = {
            'colors': f'{category}__color_id__in',
            'stones': f'{category}__stone_id__in',
            'metals': f'{category}__metal_id__in',
            'collections': f'{category}__collection_id__in',
        }

        return self._build_filters(params, filter_map)

    def _get_filters_for_product(self):
        """
        Build database filters for direct product filtering.
        """
        params = self._get_params()

        filter_map = {
            'colors': 'color_id__in',
            'stones': 'stone_id__in',
            'metals': 'metal__id__in',
            'collections': 'collection__id__in',
        }

        return self._build_filters(params, filter_map)
