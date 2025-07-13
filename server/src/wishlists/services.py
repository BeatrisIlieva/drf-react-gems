# Wishlist Services
# This module contains service classes for wishlist business logic.
# Services handle user identification, product validation, and wishlist operations.

from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
from typing import Dict, Any

from src.wishlists.models import Wishlist
from src.common.services import UserIdentificationService
from src.wishlists.constants import WishlistErrorMessages


class WishlistService:
    """
    Service class for wishlist business logic operations.
    
    This service provides methods for managing wishlist items including:
    - User identification for both authenticated and guest users
    - Product validation and retrieval
    - Wishlist item creation, retrieval, and deletion
    - Duplicate item checking
    
    All methods are static to avoid state management and ensure
    thread-safe operations across the application.
    """
    
    @staticmethod
    def get_user_identifier(
        request: Any
    ) -> Dict[str, Any]:
        """
        Get user identification filters for wishlist operations.
        
        This method delegates to UserIdentificationService to determine
        whether the request is from an authenticated user or guest user
        and returns appropriate filter parameters.
        
        Args:
            request: The HTTP request object containing user information
            
        Returns:
            Dictionary containing user identification filters:
            - For authenticated users: {'user': user_object}
            - For guest users: {'guest_id': guest_uuid}
            
        Raises:
            ValidationError: If user identification fails (e.g., missing Guest-Id header)
        """
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_product_object(
        content_type: ContentType,
        object_id: int
    ) -> Any:
        """
        Retrieve a product object using ContentType framework.
        
        This method validates that the requested product exists in the database
        and returns the actual product object for further operations.
        
        Args:
            content_type: ContentType instance for the product model
            object_id: The ID of the specific product object
            
        Returns:
            The product object instance
            
        Raises:
            NotFound: If the product with the given ID doesn't exist
        """
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound(WishlistErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def check_item_exists(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> bool:
        """
        Check if a wishlist item already exists for the user.
        
        This method prevents duplicate items in the wishlist by checking
        if the user (authenticated or guest) already has the specific
        product in their wishlist.
        
        Args:
            user_filters: Dictionary containing user identification filters
            content_type: ContentType instance for the product model
            object_id: The ID of the specific product object
            
        Returns:
            True if the item already exists in the user's wishlist, False otherwise
        """
        return Wishlist.objects.filter(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        ).exists()

    @staticmethod
    def create_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> Wishlist:
        """
        Create a new wishlist item for the user.
        
        This method creates a new wishlist item after validating that:
        1. The product exists in the database
        2. The user doesn't already have this item in their wishlist
        
        Args:
            user_filters: Dictionary containing user identification filters
            content_type: ContentType instance for the product model
            object_id: The ID of the specific product object
            
        Returns:
            The created Wishlist instance
            
        Raises:
            ValidationError: If the item already exists in the user's wishlist
            NotFound: If the product doesn't exist in the database
        """
        # Check if item already exists to prevent duplicates
        if WishlistService.check_item_exists(user_filters, content_type, object_id):
            raise ValidationError({'detail': WishlistErrorMessages.ITEM_ALREADY_EXISTS})
        
        # Validate that the product exists
        WishlistService.get_product_object(content_type, object_id)
        
        # Create the wishlist item
        created_item: Wishlist = Wishlist.objects.create(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        )
        return created_item

    @staticmethod
    def get_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> Wishlist:
        """
        Retrieve a specific wishlist item for the user.
        
        This method finds and returns a specific wishlist item for the user
        (authenticated or guest) and the specified product.
        
        Args:
            user_filters: Dictionary containing user identification filters
            content_type: ContentType instance for the product model
            object_id: The ID of the specific product object
            
        Returns:
            The Wishlist instance for the specified item
            
        Raises:
            NotFound: If the wishlist item doesn't exist for the user
        """
        try:
            item: Wishlist = Wishlist.objects.get(
                content_type=content_type,
                object_id=object_id,
                **user_filters
            )
            return item
        except Wishlist.DoesNotExist:
            raise NotFound(WishlistErrorMessages.ITEM_NOT_FOUND)

    @staticmethod
    def delete_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> bool:
        """
        Delete a wishlist item for the user.
        
        This method removes a specific wishlist item from the user's wishlist.
        It first validates that the item exists before deletion.
        
        Args:
            user_filters: Dictionary containing user identification filters
            content_type: ContentType instance for the product model
            object_id: The ID of the specific product object
            
        Returns:
            True if the item was successfully deleted
            
        Raises:
            NotFound: If the wishlist item doesn't exist for the user
        """
        # Get the wishlist item (this will raise NotFound if it doesn't exist)
        wishlist_item: Wishlist = WishlistService.get_wishlist_item(
            user_filters, content_type, object_id
        )
        
        # Delete the item
        wishlist_item.delete()
        return True
