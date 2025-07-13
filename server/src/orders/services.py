# services.py for the Orders app
# This file contains business logic for payment validation and order processing.
# Every line is documented for beginners to understand the purpose and reasoning behind each implementation.

from django.db import transaction  # For atomic database operations (all-or-nothing)
from django.db.models import QuerySet  # Type hint for querysets
from django.contrib.contenttypes.models import ContentType  # For generic relations to any model

from rest_framework.exceptions import ValidationError, NotFound  # For API error handling

from typing import Dict, Any, List
from datetime import datetime  # For date/time validation
import re  # For regex-based validation
import uuid  # For generating unique order group IDs

from src.orders.models import Order  # The Order model
from src.shopping_bags.models import ShoppingBag  # Shopping bag model for cart functionality
from src.common.services import UserIdentificationService  # Service for user identification
from src.orders.constants import CardErrorMessages, CardRegexPatterns  # Error messages and regex patterns for card validation


class PaymentValidationService:
    """
    Service class for validating payment (credit card) data.
    Provides static methods to validate card number, holder name, CVV, and expiry date.
    Ensures all payment data is correct before processing an order.
    """
    # Regex patterns for different card types
    CARD_PATTERNS: Dict[str, str] = {
        'VISA': CardRegexPatterns.VISA,
        'MASTERCARD_LEGACY': CardRegexPatterns.MASTERCARD_LEGACY,
        'MASTERCARD_NEW': CardRegexPatterns.MASTERCARD_NEW
    }
    CVV_PATTERN: str = CardRegexPatterns.CVV
    EXPIRY_DATE_PATTERN: str = CardRegexPatterns.EXPIRY_DATE
    CARD_HOLDER_PATTERN: str = CardRegexPatterns.CARD_HOLDER

    @classmethod
    def validate_card_number(
        cls,
        card_number: str
    ) -> bool:
        # Validates the card number using regex patterns for supported card types
        if not card_number:
            raise ValidationError(
                {'card_number': CardErrorMessages.INVALID_CARD_NUMBER})
        for pattern in cls.CARD_PATTERNS.values():
            if re.match(pattern, card_number):
                return True
        raise ValidationError(
            {'card_number': CardErrorMessages.INVALID_CARD_NUMBER})

    @classmethod
    def validate_card_holder_name(
        cls,
        name: str
    ) -> bool:
        # Validates the card holder's name (letters, spaces, hyphens, etc.)
        if not name:
            raise ValidationError(
                {'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME})
        if not re.match(cls.CARD_HOLDER_PATTERN, name):
            raise ValidationError(
                {'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME})
        return True

    @classmethod
    def validate_cvv(
        cls,
        cvv: str
    ) -> bool:
        # Validates the CVV (security code) for correct length and digits
        if not cvv:
            raise ValidationError({'cvv': CardErrorMessages.INVALID_CVV_CODE})
        if not re.match(cls.CVV_PATTERN, cvv):
            raise ValidationError({'cvv': CardErrorMessages.INVALID_CVV_CODE})
        return True

    @classmethod
    def validate_expiry_date(
        cls,
        expiry_date: str
    ) -> bool:
        # Validates the expiry date (MM/YY format) and checks if the card is expired
        if not expiry_date:
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})
        if not re.match(cls.EXPIRY_DATE_PATTERN, expiry_date):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})
        # Split expiry date into month and year
        month, year = expiry_date.split('/')
        current_date = datetime.now()
        current_year = current_date.year % 100  # Get last two digits of year
        current_month = current_date.month
        exp_year = int(year)
        exp_month = int(month)
        # Check if the card is expired
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.CARD_HAS_EXPIRED})
        return True

    @classmethod
    def validate_payment_data(
        cls,
        payment_data: Dict[str, str]
    ) -> bool:
        # Validates all payment fields together
        cls.validate_card_number(payment_data.get('card_number'))
        cls.validate_card_holder_name(payment_data.get('card_holder_name'))
        cls.validate_cvv(payment_data.get('cvv'))
        cls.validate_expiry_date(payment_data.get('expiry_date'))
        return True


class OrderService:
    """
    Service class for business logic related to orders.
    Handles order creation, grouping, retrieval, and total calculation.
    """
    @staticmethod
    def get_user_identifier(
        request: Any
    ) -> Dict[str, Any]:
        # Uses a shared service to extract user identification info from the request
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(
        content_type: ContentType,
        object_id: int
    ) -> Any:
        # Retrieves the product instance (inventory) for a given content type and object ID
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    @transaction.atomic  # Ensures all DB operations succeed or fail together (no partial orders)
    def process_order_from_shopping_bag(
        user: Any,
        payment_data: Dict[str, str]
    ) -> List[Order]:
        # Validates payment data before processing
        PaymentValidationService.validate_payment_data(payment_data)
        # Fetches all shopping bag items for the user
        shopping_bag_items = ShoppingBag.objects.filter(
            user=user
        ).select_related(
            'content_type'
        ).prefetch_related(
            'inventory'
        )
        # If the shopping bag is empty, raise an error
        if not shopping_bag_items.exists():
            raise ValidationError({'shopping_bag': 'Shopping bag is empty'})
        # Generate a unique order group ID for this checkout
        order_group = uuid.uuid4()
        orders: List[Order] = []
        # Create an Order for each item in the shopping bag
        for bag_item in shopping_bag_items:
            order = Order.objects.create(
                user=user,
                content_type=bag_item.content_type,
                object_id=bag_item.object_id,
                quantity=bag_item.quantity,
                order_group=order_group,
            )
            orders.append(order)
        # Clear the shopping bag after order creation
        shopping_bag_items.delete()
        return orders

    @staticmethod
    def get_user_orders(
        user: Any
    ) -> QuerySet[Order]:
        # Retrieves all orders for a user, with related product and user info
        return Order.objects.filter(
            user=user
        ).select_related(
            'content_type',
            'user'
        ).prefetch_related(
            'inventory'
        ).order_by(
            '-created_at'
        )

    @staticmethod
    def get_user_orders_grouped(
        user: Any
    ) -> Dict[str, List[Order]]:
        # Groups orders by order_group (all products purchased together)
        orders = OrderService.get_user_orders(user)
        grouped_orders: Dict[str, List[Order]] = {}
        for order in orders:
            order_group_str = str(order.order_group)
            if order_group_str not in grouped_orders:
                grouped_orders[order_group_str] = []
            grouped_orders[order_group_str].append(order)
        return grouped_orders

    @staticmethod
    def calculate_order_group_total(
        order_group_id: str,
        user: Any
    ) -> float:
        # Calculates the total price for all orders in a group (single checkout)
        orders = Order.objects.filter(
            user=user,
            order_group=order_group_id
        ).prefetch_related('inventory')
        total: float = 0.0
        for order in orders:
            if order.inventory and hasattr(order.inventory, 'price'):
                total += float(order.inventory.price) * order.quantity
        return round(total, 2)
