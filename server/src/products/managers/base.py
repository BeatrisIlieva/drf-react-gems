from django.db import models
from django.db.models import Min, Max, Avg, Count


class BaseProductManager(models.Manager):
    """
    Base manager for product models with optimized query methods.

    This manager provides methods for retrieving products using select_related and prefetch_related
    to minimize database hits and includes annotations for calculated fields like average ratings
    and stock status.

    The manager is designed to work with any product type (Earwear, Neckwear, etc.)
    and provides consistent query patterns across all product categories.
    """

    def get_product_item(self, item_id):
        """
        Retrieve a single product by its ID.

        This method provides a simple way to get a specific product
        by its primary key. It's used when displaying individual
        product details.
        """
        return self.get(pk=item_id)

    def get_product_list(self, filters, ordering):
        """
        Retrieve a filtered and ordered list of products.

        This method applies filters to the product queryset and then
        calls the optimized _get_raw_products method to add annotations
        and related data. It's used for product listing pages with
        filtering and sorting capabilities.
        """
        # Apply filters to the base queryset
        qs = self.filter(filters)

        # Get optimized product data with annotations
        raw_products = self._get_raw_products(qs, ordering)

        return raw_products

    def _get_raw_products(self, qs, ordering):
        """
        This method takes a filtered queryset and adds optimized database
        queries with select_related, prefetch_related, and annotations.
        It calculates important product data like total quantity, price
        ranges, stock status, and average ratings in a single query.
        """
        # Map user-friendly ordering parameters to database fields
        # This allows the frontend to use simple names while the database
        # uses optimized field names for sorting
        ordering_map = {
            'price_asc': 'min_price',  # Sort by lowest price first
            'price_desc': '-max_price',  # Sort by highest price first
            'rating': '-average_rating',  # Sort by highest rating first
        }

        # Get the database field name for ordering
        ordering_criteria = ordering_map[ordering]

        # Return optimized queryset with all related data
        return (
            qs
            # prefetch_related fetches many-to-many and reverse foreign key relationships
            # This prevents N+1 queries when accessing inventory and review data
            .prefetch_related('inventory', 'review')
            # values() specifies which fields to include in the result
            .values(
                'id',
                'collection__name',
                'first_image',
                'second_image',
                'third_image',
                'fourth_image',
                'color__name',
                'stone__name',
                'metal__name',
            )
            # Annotations add calculated fields to each product
            .annotate(
                # Find the lowest price for this product
                min_price=Min('inventory__price'),
                # Find the highest price for this product
                max_price=Max('inventory__price'),
                # Calculate average rating from approved reviews
                average_rating=Avg('review__rating', distinct=True),
            )
            # Order by the specified criteria, with ID as secondary sort
            .order_by(
                f'{ordering_criteria}',
                'id',
            )
        )
        
        


class BaseAttributesManager(models.Manager):
    """
    Base manager for attribute models with counting functionality.

    This manager provides methods for retrieving attributes (colors, metals,
    stones, collections) with counts of how many products use each attribute.
    It's used for building filter options in the frontend, showing users
    how many products are available for each filter choice.

    The manager supports filtering by category, allowing it to show counts
    for specific product types (e.g., only earwear, only neckwear).
    """

    def get_attributes_count(self, filters, category):
        qs = self.get_queryset()

        # Only use category if it is a valid, non-empty string
        if category and isinstance(category, str) and category.strip():
            return (
                qs.prefetch_related(category)
                .filter(filters)
                .values('id', 'name')
                .annotate(count=Count(category))
                .filter(count__gt=0)
            )

        else:
            # If no valid category, just return all attributes with count=0
            return qs.values('id', 'name').annotate(
                count=models.Value(0, output_field=models.IntegerField())
            )
