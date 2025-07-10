from typing import Any, Dict, Optional
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from src.orders.constants import CardFieldLengths
from src.orders.models import Order
from src.orders.services import OrderService, PaymentValidationService
from src.common.mixins import InventoryMixin


class OrderSerializer(serializers.ModelSerializer):
    content_type: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    product_info: serializers.SerializerMethodField = serializers.SerializerMethodField()
    product_content_type: serializers.SerializerMethodField = serializers.SerializerMethodField()
    product_object_id: serializers.SerializerMethodField = serializers.SerializerMethodField()
    total_price: serializers.SerializerMethodField = serializers.SerializerMethodField()
    status_display: serializers.CharField = serializers.CharField(
        source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields: list[str] = [
            'id',
            'user',
            'quantity',
            'status',
            'status_display',
            'created_at',
            'content_type',
            'object_id',
            'product_content_type',
            'product_object_id',
            'order_group',
            'product_info',
            'total_price',
        ]
        read_only_fields: list[str] = [
            'id',
            'created_at',
            'user',
            'order_group',
            'product_info',
            'product_content_type',
            'product_object_id',
            'total_price',
            'status_display'
        ]
        depth = 3

    def get_product_info(
        self,
        obj: Any
    ) -> Dict[str, Any]:
        return InventoryMixin.get_product_info(obj)

    def get_product_content_type(
        self,
        obj: Any
    ) -> Optional[str]:
        inventory = obj.inventory
        if not inventory:
            return None
        product = getattr(inventory, 'product', None)
        if not product:
            return None
        product_content_type = ContentType.objects.get_for_model(
            product.__class__)
        return product_content_type.model

    def get_product_object_id(
        self,
        obj: Any
    ) -> Optional[Any]:
        inventory = obj.inventory
        if not inventory:
            return None
        product = getattr(inventory, 'product', None)
        if not product:
            return None
        return product.id

    def get_total_price(
        self,
        obj: Any
    ) -> float:
        return InventoryMixin.get_total_price_per_product(obj)


class OrderGroupSerializer(serializers.Serializer):
    order_group: serializers.UUIDField = serializers.UUIDField(read_only=True)
    status: serializers.CharField = serializers.CharField(read_only=True)
    status_display: serializers.CharField = serializers.CharField(read_only=True)
    created_at: serializers.DateTimeField = serializers.DateTimeField(read_only=True)
    total_price: serializers.FloatField = serializers.FloatField(read_only=True)
    total_items: serializers.IntegerField = serializers.IntegerField(read_only=True)
    products: OrderSerializer = OrderSerializer(many=True, read_only=True)

    def to_representation(
        self,
        instance: Any
    ) -> Dict[str, Any]:
        if isinstance(instance, dict) and 'orders' in instance:
            orders = instance['orders']
            if not orders:
                return {}
            first_order = orders[0]
            total_items = sum(order.quantity for order in orders)
            return {
                'order_group': str(first_order.order_group),
                'status': first_order.status,
                'status_display': first_order.get_status_display(),
                'created_at': first_order.created_at,
                'total_price': OrderService.calculate_order_group_total(
                    str(first_order.order_group),
                    first_order.user
                ),
                'total_items': total_items,
                'products': OrderSerializer(orders, many=True).data
            }
        return super().to_representation(instance)


class OrderCreateSerializer(serializers.Serializer):
    card_number: serializers.CharField = serializers.CharField(
        max_length=CardFieldLengths.CARD_NUMBER_MAX_LENGTH)
    card_holder_name: serializers.CharField = serializers.CharField(
        max_length=CardFieldLengths.CARD_HOLDER_NAME_MAX_LENGTH)
    expiry_date: serializers.CharField = serializers.CharField(
        max_length=CardFieldLengths.EXPIRY_DATE_MAX_LENGTH)
    cvv: serializers.CharField = serializers.CharField(
        max_length=CardFieldLengths.CVV_MAX_LENGTH)

    def validate(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        PaymentValidationService.validate_payment_data({
            'card_number': data.get('card_number'),
            'card_holder_name': data.get('card_holder_name'),
            'cvv': data.get('cvv'),
            'expiry_date': data.get('expiry_date'),
        })
        return data
