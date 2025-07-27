from rest_framework import serializers

from src.orders.constants import CardFieldLengths
from src.orders.models import Order
from src.orders.services import OrderService, PaymentValidationService
from src.common.mixins import InventoryMixin


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Key Features:
    - Serializes order details, including inventory, status, and user.
    - Excludes size and quantity fields to ensure only unique products are shown in order history.
    - Includes product_info (details about the product from inventory, with size removed).
    - Includes product_content_type and product_object_id for review integration (used by frontend to submit reviews for the correct product).
    - Calculates total price for the order item.
    """

    inventory = serializers.PrimaryKeyRelatedField(
        queryset=Order._meta.get_field('inventory').related_model.objects.all()
    )
    product_info = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )
    product_content_type = serializers.SerializerMethodField()
    product_object_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'status_display',
            'created_at',
            'order_group',
            'inventory',
            'product_info',
            'total_price',
            'product_content_type',
            'product_object_id',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'user',
            'order_group',
            'product_info',
            'total_price',
            'status_display',
            'product_content_type',
            'product_object_id',
        ]
        depth = 3

    def get_product_info(self, obj):
        """
        Returns product details for the order item, using the related inventory's product.
        Removes size from the product_info if present.
        """
        info = InventoryMixin.get_product_info(obj)
        if isinstance(info, dict) and 'size' in info:
            info.pop('size')

        return info

    def get_total_price(self, obj):
        """
        Calculates the total price for this order item (price * quantity).
        """
        return InventoryMixin.get_total_price_per_product(obj)

    def get_product_content_type(self, obj):
        """
        Returns the model name of the related product (e.g., 'earwear'), used for review integration.
        """
        inventory = obj.inventory
        if not inventory:
            return None

        product = getattr(inventory, 'product', None)
        if not product:
            return None

        return product._meta.model_name

    def get_product_object_id(self, obj):
        """
        Returns the primary key of the related product, used for review integration.
        """
        inventory = obj.inventory
        if not inventory:
            return None

        product = getattr(inventory, 'product', None)
        if not product:
            return None

        return product.id


class OrderGroupSerializer(serializers.Serializer):
    """
    Serializer for a group of orders (products purchased together in one checkout).
    Aggregates order info, total price, and product details for the group.
    """

    order_group = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    products = OrderSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """
        Customizes the output format for grouped orders.
        """
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
                    str(first_order.order_group), first_order.user
                ),
                'total_items': total_items,
                'products': OrderSerializer(orders, many=True).data,
            }

        return super().to_representation(instance)


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating an order from payment data.
    Validates credit card and payment info before processing the order.
    """

    card_number = serializers.CharField(
        max_length=CardFieldLengths.CARD_NUMBER_MAX_LENGTH
    )
    card_holder_name = serializers.CharField(
        max_length=CardFieldLengths.CARD_HOLDER_NAME_MAX_LENGTH
    )
    expiry_date = serializers.CharField(
        max_length=CardFieldLengths.EXPIRY_DATE_MAX_LENGTH
    )
    cvv = serializers.CharField(max_length=CardFieldLengths.CVV_MAX_LENGTH)

    def validate(self, data):
        """
        Uses PaymentValidationService to check all payment fields for validity.
        """
        PaymentValidationService.validate_payment_data(
            {
                'card_number': data.get('card_number'),
                'card_holder_name': data.get('card_holder_name'),
                'cvv': data.get('cvv'),
                'expiry_date': data.get('expiry_date'),
            }
        )

        return data
