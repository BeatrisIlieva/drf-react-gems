# Shopping Bag Services
# This module contains business logic for shopping bag operations.
# Services handle complex operations like inventory validation, quantity updates, and user identification.

from django.db import transaction
from django.db.models import F
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError, NotFound

from typing import Dict, Any
from django.http import HttpRequest

from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService
from src.shopping_bags.constants import ShoppingBagErrorMessages


class ShoppingBagService:
    """
    Service class for shopping bag operations.
    
    This class encapsulates all business logic related to shopping bag functionality,
    including user identification, inventory validation, and quantity management.
    
    Key Responsibilities:
    - User identification (authenticated vs guest users)
    - Inventory object retrieval and validation
    - Stock quantity validation
    - Atomic database operations for inventory updates
    - Shopping bag item creation and retrieval
    """
    
    @staticmethod
    def get_user_identifier(request: HttpRequest) -> Dict[str, Any]:
        """
        Get user identifier for shopping bag operations.
        
        This method determines whether the request is from an authenticated user
        or a guest user and returns appropriate filter parameters for database queries.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Dictionary containing filter parameters for user identification
            (either 'user' for authenticated users or 'guest_id' for guests)
        """
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(content_type: ContentType, object_id: int) -> Any:
        """
        Retrieve an inventory object by content type and object ID.
        
        This method uses Django's ContentType framework to dynamically retrieve
        any type of inventory object (earwear, necklaces, etc.) without knowing
        the specific model class in advance.
        
        Args:
            content_type: The ContentType instance identifying the model
            object_id: The primary key of the inventory object
            
        Returns:
            The inventory object instance
            
        Raises:
            NotFound: If the inventory object doesn't exist
        """
        try:
            # get_object_for_this_type() is a ContentType method that retrieves
            # the actual object instance based on the content_type and object_id
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            # Raise a NotFound exception with a user-friendly error message
            raise NotFound(ShoppingBagErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def validate_inventory_quantity(inventory_obj: Any, required_quantity: int) -> None:
        """
        Validate that the required quantity is available in stock.
        
        This method checks if there's enough inventory to fulfill the request.
        It prevents users from adding more items than are available in stock.
        
        Args:
            inventory_obj: The inventory object to check
            required_quantity: The quantity being requested
            
        Raises:
            ValidationError: If insufficient stock is available
        """
        if required_quantity > inventory_obj.quantity:
            # Format the error message with the actual available quantity
            raise ValidationError({
                'quantity': ShoppingBagErrorMessages.INSUFFICIENT_STOCK.format(quantity=inventory_obj.quantity)
            })

    @staticmethod
    @transaction.atomic
    def update_inventory_quantity(inventory_obj: Any, delta: int) -> None:
        """
        Update inventory quantity using atomic database operations.
        
        This method uses F() expressions to ensure thread-safe quantity updates.
        The @transaction.atomic decorator ensures that the entire operation
        either succeeds completely or fails completely (no partial updates).
        
        Args:
            inventory_obj: The inventory object to update
            delta: The change in quantity (positive for additions, negative for removals)
        """
        # F() expression ensures the database operation is atomic
        # This prevents race conditions when multiple users update inventory simultaneously
        inventory_obj.quantity = F('quantity') - delta
        inventory_obj.save(update_fields=['quantity'])
        # Refresh from database to get the updated value
        inventory_obj.refresh_from_db()

    @staticmethod
    def get_or_create_bag_item(filters: Dict[str, Any], defaults: Dict[str, Any]) -> tuple[ShoppingBag, bool]:
        """
        Get or create a shopping bag item.
        
        This method uses Django's get_or_create() to either retrieve an existing
        shopping bag item or create a new one if it doesn't exist.
        
        Args:
            filters: Dictionary of filters to find existing item
            defaults: Dictionary of default values for new item creation
            
        Returns:
            Tuple of (ShoppingBag instance, created boolean)
            The boolean indicates whether a new item was created (True) or retrieved (False)
        """
        return ShoppingBag.objects.get_or_create(**filters, defaults=defaults)
