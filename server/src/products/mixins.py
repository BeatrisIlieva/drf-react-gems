from django.db import models
from django.db.models import Q
from typing import Dict
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
    NAME_MAX_LENGTH: int = NameFieldLengths.NAME_MAX_LENGTH

    class Meta:
        # Abstract = True means this model won't create its own database table
        # It's only used as a base class for other models
        abstract = True

    # Standardized name field used across multiple entities
    # unique=True ensures no duplicate names within the same entity type
    # max_length uses the constant for consistency
    name: models.CharField = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class FilterMixin:
    """
    Mixin class that provides filtering functionality for product listings.

    This mixin is used by views that need to filter products based on
    various attributes like colors, stones, metals, and collections.
    It provides methods to extract filter parameters from request query
    strings and build database queries.

    The mixin supports both filtering by product attributes directly
    and filtering by related inventory attributes,
    """

    def _get_params(self) -> Dict[str, list[str]]:
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

    def _get_filters_for_attributes(self, category: str) -> Q:
        """
        Build database filters for attribute-based filtering.

        This method creates Django Q objects for filtering products
        based on their attributes (color, stone, metal, collection).
        It's used when filtering products that have these attributes
        directly (like when viewing a specific product category).
        """
        # Get the filter parameters from the request
        params: Dict[str, list[str]] = self._get_params()
        # Initialize an empty Q object to build filters
        filters: Q = Q()

        # Add color filter if colors are specified
        if params['colors']:
            # Filter by color_id in the specified colors list
            filters &= Q(**{f'{category}__color_id__in': params['colors']})

        # Add stone filter if stones are specified
        if params['stones']:
            # Filter by stone_id in the specified stones list
            filters &= Q(**{f'{category}__stone_id__in': params['stones']})

        # Add metal filter if metals are specified
        if params['metals']:
            # Filter by metal_id in the specified metals list
            filters &= Q(**{f'{category}__metal_id__in': params['metals']})

        # Add collection filter if collections are specified
        if params['collections']:
            # Filter by collection_id in the specified collections list
            filters &= Q(
                **{f'{category}__collection_id__in': params['collections']})

        return filters

    def _get_filters_for_product(self) -> Q:
        """
        Build database filters for direct product filtering.

        This method creates Django Q objects for filtering products
        directly by their attributes. It's used when the view is
        already working with a specific product type and doesn't need
        the category prefix in the filter.
        """
        # Get the filter parameters from the request
        params: Dict[str, list[str]] = self._get_params()
        # Initialize an empty Q object to build filters
        filters: Q = Q()

        # Add color filter if colors are specified
        if params['colors']:
            # Filter by color_id directly on the product
            filters &= Q(color_id__in=params['colors'])

        # Add stone filter if stones are specified
        if params['stones']:
            # Filter by stone_id directly on the product
            filters &= Q(stone_id__in=params['stones'])

        # Add metal filter if metals are specified
        if params['metals']:
            # Filter by metal_id directly on the product
            filters &= Q(metal__id__in=params['metals'])

        # Add collection filter if collections are specified
        if params['collections']:
            # Filter by collection_id directly on the product
            filters &= Q(collection__id__in=params['collections'])

        return filters
