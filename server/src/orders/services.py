from django.db import transaction
from django.db.models import F, Sum, QuerySet
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
from typing import Dict, Any, List
from datetime import datetime
import re
import uuid

from src.orders.models import Order
from src.shopping_bags.models import ShoppingBag
from src.orders.choices import OrderStatusChoices
from src.common.services import UserIdentificationService


class PaymentValidationService:
    """Service for validating payment card details."""

    CARD_PATTERNS = {
        'VISA': r'^4[0-9]{3} [0-9]{4} [0-9]{4} [0-9]{4}$',
        'MASTERCARD_51': r'^51[0-9]{2} [0-9]{4} [0-9]{4} [0-9]{4}$',
        'MASTERCARD_55': r'^55[0-9]{2} [0-9]{4} [0-9]{4} [0-9]{4}$',
        'MASTERCARD_222': r'^222[0-9]{1} [0-9]{4} [0-9]{4} [0-9]{4}$',
        'MASTERCARD_227': r'^227[0-9]{1} [0-9]{4} [0-9]{4} [0-9]{4}$',
        'MASTERCARD_27': r'^27[0-9]{2} [0-9]{4} [0-9]{4} [0-9]{4}$'
    }

    CVV_PATTERN = r'^[0-9]{3}$'
    EXPIRY_DATE_PATTERN = r'^(0[1-9]|1[0-2])/([0-9]{2})$'
    CARD_HOLDER_PATTERN = r"^[A-Za-z\u00C0-\u024F'\- ]{2,50}$"

    @classmethod
    def validate_card_number(cls, card_number: str) -> bool:
        """Validate card number against known patterns."""
        if not card_number:
            raise ValidationError({'card_number': 'Card number is required'})

        for pattern in cls.CARD_PATTERNS.values():
            if re.match(pattern, card_number):
                return True

        raise ValidationError(
            {'card_number': 'Please enter a valid card number'})

    @classmethod
    def validate_card_holder_name(cls, name: str) -> bool:
        """Validate card holder name."""
        if not name:
            raise ValidationError(
                {'card_holder_name': 'Card holder name is required'})

        if not re.match(cls.CARD_HOLDER_PATTERN, name):
            raise ValidationError(
                {'card_holder_name': 'Please enter a valid name'})

        return True

    @classmethod
    def validate_cvv(cls, cvv: str) -> bool:
        """Validate CVV."""
        if not cvv:
            raise ValidationError({'cvv': 'CVV is required'})

        if not re.match(cls.CVV_PATTERN, cvv):
            raise ValidationError(
                {'cvv': 'Please enter a valid security code'})

        return True

    @classmethod
    def validate_expiry_date(cls, expiry_date: str) -> bool:
        """Validate expiry date and check if card is expired."""
        if not expiry_date:
            raise ValidationError({'expiry_date': 'Expiry date is required'})

        if not re.match(cls.EXPIRY_DATE_PATTERN, expiry_date):
            raise ValidationError(
                {'expiry_date': 'Please enter a valid expiry date (MM/YY)'})

        month, year = expiry_date.split('/')
        current_date = datetime.now()
        current_year = current_date.year % 100
        current_month = current_date.month

        exp_year = int(year)
        exp_month = int(month)

        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            raise ValidationError({'expiry_date': 'Card has expired'})

        return True

    @classmethod
    def validate_payment_data(cls, payment_data: Dict[str, str]) -> bool:
        """Validate all payment fields."""
        cls.validate_card_number(payment_data.get('card_number'))
        cls.validate_card_holder_name(payment_data.get('card_holder_name'))
        cls.validate_cvv(payment_data.get('cvv'))
        cls.validate_expiry_date(payment_data.get('expiry_date'))
        return True


class OrderService:
    """Service for handling order operations."""

    @staticmethod
    def get_user_identifier(request) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(content_type: ContentType, object_id: int):
        """Get inventory object from content type and object id."""
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    @transaction.atomic
    def process_order_from_shopping_bag(user, payment_data: Dict[str, str]) -> List[Order]:
        """
        Process order by transferring shopping bag items to orders.
        Validates payment and creates order records with the same order_group UUID.
        """
        # Validate payment data
        PaymentValidationService.validate_payment_data(payment_data)

        # Get user's shopping bag items
        shopping_bag_items = ShoppingBag.objects.filter(
            user=user
        ).select_related('content_type').prefetch_related('inventory')

        if not shopping_bag_items.exists():
            raise ValidationError({'shopping_bag': 'Shopping bag is empty'})

        # Generate a single order group UUID for all items in this order
        order_group = uuid.uuid4()
        orders = []

        for bag_item in shopping_bag_items:
            # Create order from shopping bag item with the same order_group
            order = Order.objects.create(
                user=user,
                content_type=bag_item.content_type,
                object_id=bag_item.object_id,
                quantity=bag_item.quantity,
                order_group=order_group,
                # Default status is PENDING, so we don't need to set it explicitly
            )
            orders.append(order)

        # Delete shopping bag items after successful order creation
        shopping_bag_items.delete()

        return orders

    @staticmethod
    def get_user_orders(user) -> QuerySet[Order]:
        """Get all orders for a user."""
        return Order.objects.filter(
            user=user
        ).select_related('content_type', 'user').prefetch_related('inventory').order_by('-created_at')

    @staticmethod
    def get_user_orders_grouped(user) -> Dict[str, List[Order]]:
        """Get user orders grouped by order_group UUID."""
        orders = OrderService.get_user_orders(user)
        grouped_orders = {}
        
        for order in orders:
            order_group_str = str(order.order_group)
            if order_group_str not in grouped_orders:
                grouped_orders[order_group_str] = []
            grouped_orders[order_group_str].append(order)
        
        return grouped_orders

    @staticmethod
    def calculate_order_group_total(order_group_id: str, user) -> float:
        """Calculate total price for all products in an order group."""
        orders = Order.objects.filter(
            user=user,
            order_group=order_group_id
        ).prefetch_related('inventory')
        
        total = 0.0
        for order in orders:
            if order.inventory and hasattr(order.inventory, 'price'):
                total += float(order.inventory.price) * order.quantity
        
        return round(total, 2)


class InventoryMixin:
    """Mixin for common inventory operations shared between ShoppingBag and Order."""

    @staticmethod
    def get_product_info(obj):
        """Get product information from inventory object."""
        inventory = obj.inventory
        if not inventory:
            return {}

        product = getattr(inventory, 'product', None)
        if not product:
            return {}

        product_content_type = ContentType.objects.get_for_model(
            product.__class__
        )
        model_name = product_content_type.model.capitalize()

        return {
            'product_id': product.id,
            'collection': str(product.collection),
            'price': float(inventory.price),
            'first_image': product.first_image,
            'available_quantity': inventory.quantity,
            'size': str(getattr(inventory, 'size', '')),
            'metal': str(product.metal.name),
            'stone': str(product.stone.name),
            'color': str(product.color.name),
            'category': model_name,
        }

    @staticmethod
    def get_total_price_per_product(obj):
        """Calculate total price for the item."""
        try:
            return round(obj.inventory.price * obj.quantity, 2)
        except Exception:
            return 0