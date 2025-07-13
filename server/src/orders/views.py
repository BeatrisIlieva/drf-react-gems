# views.py for the Orders app
# This file defines the API endpoints for order management using Django REST Framework (DRF).
# Every line is documented for beginners to understand the purpose and reasoning behind each implementation.

from typing import Any
from django.db import transaction  # For atomic database operations (all-or-nothing)

from rest_framework import viewsets, status  # DRF base classes and status codes
from rest_framework.decorators import action  # For custom actions on viewsets
from rest_framework.response import Response  # For API responses
from rest_framework.exceptions import ValidationError  # For API error handling
from rest_framework.request import Request  # Type hint for requests

from src.orders.serializers import OrderCreateSerializer, OrderGroupSerializer  # Serializers for order logic
from src.orders.services import OrderService  # Business logic for orders
from src.orders.constants import OrderStatusMessages  # User-facing status messages


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for managing orders.
    - Allows users to view their orders (list, retrieve)
    - Provides a custom action to create orders from the shopping bag
    - Uses DRF's ViewSet for clean, RESTful API design
    """
    serializer_class = OrderGroupSerializer  # Default serializer for responses

    def get_queryset(
        self
    ) -> Any:
        # Returns all orders for the current user
        return OrderService.get_user_orders(self.request.user)

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        # Returns a grouped list of all orders for the current user
        grouped_orders = OrderService.get_user_orders_grouped(request.user)

        serializer_data = []
        # Each group is a set of products purchased together
        for _, orders in grouped_orders.items():
            serializer_data.append({
                'orders': orders
            })

        serializer = OrderGroupSerializer(serializer_data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,  # This action is not for a single order, but for the collection
        methods=['post'],  # Only POST requests are allowed
        url_path='create-from-bag'  # URL will be /orders/create-from-bag/
    )
    @transaction.atomic  # Ensures all DB operations succeed or fail together (no partial orders)
    def create_from_shopping_bag(
        self,
        request: Request
    ) -> Response:
        # Handles order creation from the user's shopping bag
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Process the order using validated payment data
                orders = OrderService.process_order_from_shopping_bag(
                    user=request.user,
                    payment_data=serializer.validated_data
                )

                if orders:
                    # If orders were created, calculate the total price for the group
                    order_group_str = str(orders[0].order_group)
                    total_price = OrderService.calculate_order_group_total(
                        order_group_str, request.user
                    )

                    group_serializer = OrderGroupSerializer({
                        'orders': orders
                    })

                    return Response({
                        'message': OrderStatusMessages.STATUS_CREATED,
                        'order': group_serializer.data,
                        'total_items': len(orders),
                        'total_price': total_price
                    }, status=status.HTTP_201_CREATED)
                else:
                    # No orders were created (should not happen in normal flow)
                    return Response({
                        'message': OrderStatusMessages.STATUS_NO_ORDERS,
                    }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                # Handles validation errors (e.g., invalid payment, empty bag)
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Handles serializer validation errors (e.g., missing fields)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
