from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from src.orders.models import Order
from src.orders.services import InventoryMixin, OrderService


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model with product information."""

    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    product_info = serializers.SerializerMethodField()
    product_content_type = serializers.SerializerMethodField()
    product_object_id = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display', read_only=True)

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
        """Get product information using the mixin."""
        return InventoryMixin.get_product_info(obj)

    def get_product_content_type(self, obj):
        """Get the content type of the actual product (not inventory)."""
        inventory = obj.inventory
        if not inventory:
            return None
        
        product = getattr(inventory, 'product', None)
        if not product:
            return None
        
        product_content_type = ContentType.objects.get_for_model(product.__class__)
        return product_content_type.model

    def get_product_object_id(self, obj):
        """Get the ID of the actual product (not inventory)."""
        inventory = obj.inventory
        if not inventory:
            return None
        
        product = getattr(inventory, 'product', None)
        if not product:
            return None
        
        return product.id

    def get_total_price(self, obj):
        """Get total price per product using the mixin."""
        return InventoryMixin.get_total_price_per_product(obj)


class OrderGroupSerializer(serializers.Serializer):
    """Serializer for grouped orders by order_group UUID."""

    order_group = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    products = OrderSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """
        Custom representation for grouped orders.
        instance should be a dict with 'order_group' key and list of orders as value.
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
                    str(first_order.order_group),
                    first_order.user
                ),
                'total_items': total_items,
                'products': OrderSerializer(orders, many=True).data
            }

        return super().to_representation(instance)


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating orders from shopping bag with payment data."""

    card_number = serializers.CharField(max_length=19)
    card_holder_name = serializers.CharField(max_length=50)
    expiry_date = serializers.CharField(max_length=5)
    cvv = serializers.CharField(max_length=3)

    def validate_card_number(self, value):
        """Validate card number format."""
        if not value or len(value.replace(' ', '')) < 13:
            raise serializers.ValidationError(
                "Please enter a valid card number")
        return value

    def validate_card_holder_name(self, value):
        """Validate card holder name."""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Please enter a valid name")
        return value

    def validate_cvv(self, value):
        """Validate CVV."""
        if not value or len(value) != 3 or not value.isdigit():
            raise serializers.ValidationError(
                "Please enter a valid security code")
        return value

    def validate_expiry_date(self, value):
        """Validate expiry date format."""
        if not value or len(value) != 5 or '/' not in value:
            raise serializers.ValidationError(
                "Please enter a valid expiry date (MM/YY)")
        return value
