from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from src.orders.models import Order
from src.orders.serializers import OrderSerializer, OrderCreateSerializer, OrderGroupSerializer
from src.orders.services import OrderService


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for handling order operations.
    Provides list and retrieve operations for orders.
    """
    serializer_class = OrderGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get orders for the authenticated user."""
        return OrderService.get_user_orders(self.request.user)

    def list(self, request, *args, **kwargs):
        """List orders grouped by order_group UUID."""
        grouped_orders = OrderService.get_user_orders_grouped(request.user)
        
        # Transform the grouped orders into a format suitable for serialization
        serializer_data = []
        for order_group, orders in grouped_orders.items():
            serializer_data.append({
                'orders': orders
            })
        
        serializer = OrderGroupSerializer(serializer_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create-from-bag')
    @transaction.atomic
    def create_from_shopping_bag(self, request):
        """
        Create orders from shopping bag items after payment validation.
        """
        if not request.user.is_authenticated:
            raise ValidationError(
                {'user': 'Authentication required to complete order'})

        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                orders = OrderService.process_order_from_shopping_bag(
                    user=request.user,
                    payment_data=serializer.validated_data
                )

                # Create the grouped response
                if orders:
                    order_group_str = str(orders[0].order_group)
                    total_price = OrderService.calculate_order_group_total(
                        order_group_str, request.user
                    )
                    
                    group_serializer = OrderGroupSerializer({
                        'orders': orders
                    })

                    return Response({
                        'message': 'Order completed successfully',
                        'order': group_serializer.data,
                        'total_items': len(orders),
                        'total_price': total_price
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'message': 'No orders created',
                    }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='summary')
    def get_order_summary(self, request):
        """Get order summary statistics for the user."""
        orders = self.get_queryset()

        total_orders = orders.count()
        pending_orders = orders.filter(status='PE').count()
        completed_orders = orders.filter(status='CO').count()

        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders
        })
