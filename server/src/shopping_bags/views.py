# Shopping Bag Views
# This module contains the ShoppingBagViewSet which handles all shopping bag API operations.
# The ViewSet provides CRUD operations and additional custom actions for shopping bag management.

from typing import Any
from django.db import transaction
from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.serializers import ShoppingBagSerializer
from src.shopping_bags.services import ShoppingBagService
from src.shopping_bags.constants import ShoppingBagErrorMessages


class ShoppingBagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for shopping bag operations.
    
    This ViewSet provides full CRUD operations for shopping bag items and additional
    custom actions for getting bag count and total price. It supports both authenticated
    and guest users through the UserIdentificationService.
    
    Key Features:
    - Full CRUD operations for shopping bag items
    - Automatic inventory validation and updates
    - Support for both authenticated and guest users
    - Custom actions for bag count and total price
    - Atomic transactions for data consistency
    """
    
    serializer_class = ShoppingBagSerializer
    # AllowAny permission allows both authenticated and guest users to access the API
    # This is necessary since shopping bags work for both user types
    permission_classes = [AllowAny]

    def get_queryset(self) -> Any:
        """
        Get the queryset for shopping bag items.
        
        This method filters shopping bag items based on the user (authenticated or guest)
        and includes related objects for efficient database queries.
        
        Returns:
            Filtered queryset of shopping bag items for the current user
        """
        try:
            # Get user identification filters (user_id for authenticated, guest_id for guests)
            user_filters = ShoppingBagService.get_user_identifier(self.request)
            return ShoppingBag.objects.filter(
                **user_filters
            ).select_related(
                # select_related() performs a SQL JOIN to fetch related objects
                # This reduces the number of database queries
                'content_type',
                'user'
            ).prefetch_related(
                # prefetch_related() performs a separate query to fetch related objects
                # This is used for GenericForeignKey relationships
                'inventory'
            )
        except ValidationError:
            # Return empty queryset if user identification fails
            return ShoppingBag.objects.none()

    @transaction.atomic
    def perform_create(self, serializer: Any) -> None:
        """
        Create a new shopping bag item with inventory validation.
        
        This method handles the creation of shopping bag items with proper inventory
        validation and quantity updates. It uses atomic transactions to ensure data consistency.
        
        Args:
            serializer: The validated serializer instance
        """
        # Get user identification filters
        user_filters = ShoppingBagService.get_user_identifier(self.request)
        validated_data = serializer.validated_data
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']
        quantity_to_add = validated_data['quantity']
        
        # Get the inventory object and validate stock availability
        inventory_obj = ShoppingBagService.get_inventory_object(
            content_type, object_id
        )
        ShoppingBagService.validate_inventory_quantity(
            inventory_obj, quantity_to_add)
        
        # Create filters for finding existing bag item
        filters = {
            'content_type': content_type,
            'object_id': object_id,
            **user_filters
        }
        
        # Get or create the bag item
        bag_item, created = ShoppingBagService.get_or_create_bag_item(
            filters=filters,
            defaults={'quantity': quantity_to_add}
        )
        
        if not created:
            # If item already exists, add to existing quantity
            new_total_quantity = bag_item.quantity + quantity_to_add
            # Re-validate to ensure we don't exceed stock
            ShoppingBagService.validate_inventory_quantity(
                inventory_obj, quantity_to_add
            )
            bag_item.quantity = new_total_quantity
            bag_item.save(update_fields=['quantity'])
        
        # Update inventory quantity (reduce available stock)
        ShoppingBagService.update_inventory_quantity(
            inventory_obj, quantity_to_add
        )
        
        # Set the instance for the serializer
        serializer.instance = bag_item

    @transaction.atomic
    def perform_update(self, serializer: Any) -> None:
        """
        Update a shopping bag item with inventory validation.
        
        This method handles updating shopping bag item quantities with proper
        inventory validation. If quantity becomes 0 or negative, it deletes the item.
        
        Args:
            serializer: The validated serializer instance
        """
        instance = self.get_object()
        new_quantity = serializer.validated_data.get(
            'quantity', instance.quantity
        )
        
        # If quantity is 0 or negative, delete the item
        if new_quantity <= 0:
            return self.perform_destroy(instance)
        
        # Get inventory object for validation
        inventory_obj = ShoppingBagService.get_inventory_object(
            instance.content_type, instance.object_id
        )
        
        # Calculate the change in quantity
        quantity_delta = new_quantity - instance.quantity
        
        # If adding more items, validate stock availability
        if quantity_delta > 0:
            ShoppingBagService.validate_inventory_quantity(
                inventory_obj, quantity_delta
            )
        
        # Update inventory quantity
        ShoppingBagService.update_inventory_quantity(
            inventory_obj, quantity_delta
        )
        
        # Save the updated instance
        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance: Any) -> None:
        """
        Delete a shopping bag item and restore inventory.
        
        This method handles the deletion of shopping bag items and restores
        the corresponding inventory quantity.
        
        Args:
            instance: The shopping bag item to delete
        """
        # Get inventory object to restore quantity
        inventory_obj = ShoppingBagService.get_inventory_object(
            instance.content_type, instance.object_id
        )
        
        # Restore inventory quantity (add back to available stock)
        ShoppingBagService.update_inventory_quantity(
            inventory_obj, -instance.quantity
        )
        
        # Delete the shopping bag item
        instance.delete()

    @action(
        detail=False,
        methods=['get'],
        url_path='count'
    )
    def get_bag_count(self, request: Request) -> Response:
        """
        Get the total count of items in the shopping bag.
        
        This custom action calculates the total quantity of all items in the user's
        shopping bag, regardless of product type.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response with the total count of items in the bag
        """
        try:
            # Get user identification filters
            user_filters = ShoppingBagService.get_user_identifier(request)
            
            # Aggregate the sum of all quantities in the user's bag
            count = ShoppingBag.objects.filter(**user_filters).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            return Response({'count': count}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='total-price'
    )
    def get_total_price(self, request: Request) -> Response:
        """
        Get the total price of all items in the shopping bag.
        
        This custom action calculates the total cost of all items in the user's
        shopping bag by multiplying each item's price by its quantity.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response with the total price of all items in the bag
        """
        try:
            # Get user identification filters
            user_filters = ShoppingBagService.get_user_identifier(request)
            
            # Get all bag items with their inventory information
            bag_items = ShoppingBag.objects.filter(**user_filters).select_related(
                'content_type'
            )
            
            # Calculate total price by summing (price * quantity) for each item
            total_price = sum(
                float(item.inventory.price) * item.quantity
                for item in bag_items
                if item.inventory and hasattr(item.inventory, 'price')
            )
            
            return Response({
                'total_price': round(total_price, 2)
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # Handle any unexpected errors during price calculation
            return Response({
                'error': ShoppingBagErrorMessages.ERROR_TOTAL_PRICE
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
