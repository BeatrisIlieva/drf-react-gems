"""
This module defines the API views for order management.

Key features:
- Allows users to view their orders (list, retrieve)
- Provides a custom endpoint to create orders from the shopping bag using a POST request
- Ensures all order creation steps are performed atomically (all succeed or all fail)
"""

from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from src.orders.serializers import OrderCreateSerializer, OrderGroupSerializer
from src.orders.services import OrderService
from src.orders.constants import OrderStatusMessages


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user order management.

    Inherits from DRF's ReadOnlyModelViewSet, which provides only the 'list' and 'retrieve' actions (GET requests).
    This means users can view their orders but cannot create, update, or delete them through the standard API endpoints.
    This is appropriate because order creation is handled by a custom workflow (create_from_shopping_bag),
    and we want to prevent direct modification of orders via the API.

    - Allows users to view their orders (list, retrieve)
    - Provides a custom action to create orders from the shopping bag
    - Uses @action to add a custom endpoint (not standard CRUD)
    - Uses @transaction.atomic to ensure all DB changes for order creation are all-or-nothing
    """

    serializer_class = OrderGroupSerializer

    def get_queryset(self):
        # Returns all orders for the current user
        return OrderService.get_user_orders(self.request.user)

    def list(self, request, *args, **kwargs):
        # Returns a grouped list of all orders for the current user
        grouped_orders = OrderService.get_user_orders_grouped(request.user)

        serializer_data = []
        # Each group is a set of products purchased together
        for _, orders in grouped_orders.items():
            serializer_data.append({'orders': orders})

        serializer = OrderGroupSerializer(serializer_data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,  # This action is not for a single order, but for the collection
        methods=['post'],  # Only POST requests are allowed
        url_path='create-from-bag',  # URL will be /orders/create-from-bag/
    )
    # Ensures all DB operations succeed or fail together (no partial orders)
    @transaction.atomic
    def create_from_shopping_bag(self, request):
        """
        Custom endpoint to create an order from the user's shopping bag.

        - Uses @action to expose this as a POST endpoint at /orders/create-from-bag/
        - Uses @transaction.atomic to guarantee that all database changes (order creation, inventory updates, etc.)
          are performed as a single transaction. If any step fails, all changes are rolled back, preventing partial orders.
        - Handles validation, order processing, and returns a summary of the created order group.
        """
        # Handles order creation from the user's shopping bag
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Process the order using validated payment data
                orders = OrderService.process_order_from_shopping_bag(
                    user=request.user, payment_data=serializer.validated_data
                )

                if orders:
                    # If orders were created, calculate the total price for the group
                    order_group_str = str(orders[0].order_group)
                    total_price = OrderService.calculate_order_group_total(
                        order_group_str, request.user
                    )

                    group_serializer = OrderGroupSerializer({'orders': orders})

                    return Response(
                        {
                            'message': OrderStatusMessages.STATUS_CREATED,
                            'order': group_serializer.data,
                            'total_items': len(orders),
                            'total_price': total_price,
                        },
                        status=status.HTTP_201_CREATED,
                    )

                else:
                    # No orders were created (should not happen in normal flow)
                    return Response(
                        {
                            'message': OrderStatusMessages.STATUS_NO_ORDERS,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except ValidationError as e:
                # Handles validation errors (e.g., invalid payment, empty bag)
                return Response(
                    {
                        'error': str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            # Handles serializer validation errors (e.g., missing fields)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
