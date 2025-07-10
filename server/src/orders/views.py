from typing import Any
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from src.orders.serializers import OrderCreateSerializer, OrderGroupSerializer
from src.orders.services import OrderService
from src.orders.constants import OrderStatusMessages


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderGroupSerializer

    def get_queryset(
        self
    ) -> Any:
        return OrderService.get_user_orders(self.request.user)

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        grouped_orders = OrderService.get_user_orders_grouped(request.user)

        serializer_data = []
        for _, orders in grouped_orders.items():
            serializer_data.append({
                'orders': orders
            })

        serializer = OrderGroupSerializer(serializer_data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='create-from-bag'
    )
    @transaction.atomic
    def create_from_shopping_bag(
        self,
        request: Request
    ) -> Response:
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                orders = OrderService.process_order_from_shopping_bag(
                    user=request.user,
                    payment_data=serializer.validated_data
                )

                if orders:
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
                    return Response({
                        'message': OrderStatusMessages.STATUS_NO_ORDERS,
                    }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
