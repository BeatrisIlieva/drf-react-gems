from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from src.orders.constants import CardFieldLengths
from src.orders.models import Order
from src.orders.services import OrderService, PaymentValidationService
from src.common.mixins import InventoryMixin

class OrderSerializer(serializers.ModelSerializer):
    """
    Adds extra fields and methods to provide detailed product and order info in API responses.
    """
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    product_info = serializers.SerializerMethodField()
    product_content_type = serializers.SerializerMethodField()
    product_object_id = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
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
        read_only_fields = [
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

    def get_product_info(self, obj):
        # Uses InventoryMixin to extract product details for the order

        return InventoryMixin.get_product_info(obj)

    def get_product_content_type(self, obj):
        # Returns the model name of the related product (e.g., 'earwear')
        inventory = obj.inventory
        if not inventory:
            return None

        product = getattr(inventory, 'product', None)
        if not product:
            return None

        product_content_type = ContentType.objects.get_for_model(product.__class__)

        return product_content_type.model

    def get_product_object_id(self, obj):
        # Returns the primary key of the related product
        inventory = obj.inventory
        if not inventory:
            return None

        product = getattr(inventory, 'product', None)
        if not product:
            return None

        return product.id

    def get_total_price(self, obj):
        # Uses InventoryMixin to calculate total price for this order

        return InventoryMixin.get_total_price_per_product(obj)

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
        # Customizes the output format for grouped orders
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

        # Fallback to default representation

        return super().to_representation(instance)

class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating an order from payment data.
    Validates credit card and payment info before processing the order.
    """
    card_number = serializers.CharField(max_length=CardFieldLengths.CARD_NUMBER_MAX_LENGTH)
    card_holder_name = serializers.CharField(max_length=CardFieldLengths.CARD_HOLDER_NAME_MAX_LENGTH)
    expiry_date = serializers.CharField(max_length=CardFieldLengths.EXPIRY_DATE_MAX_LENGTH)
    cvv = serializers.CharField(max_length=CardFieldLengths.CVV_MAX_LENGTH)

    def validate(self, data):
        # Uses PaymentValidationService to check all payment fields for validity
        PaymentValidationService.validate_payment_data({
            'card_number': data.get('card_number'),
            'card_holder_name': data.get('card_holder_name'),
            'cvv': data.get('cvv'),
            'expiry_date': data.get('expiry_date'),
        })

        return data