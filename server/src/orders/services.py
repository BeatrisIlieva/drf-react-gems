from django.db import transaction

from rest_framework.exceptions import ValidationError, NotFound

from datetime import datetime
import re
import uuid

from src.orders.models import Order
from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService
from src.orders.constants import CardErrorMessages, CardRegexPatterns


class PaymentValidationService:
    """
    Service class for validating payment (credit card) data.
    Provides static methods to validate card number, holder name, CVV, and expiry date.
    Ensures all payment data is correct before processing an order.
    """
    # Regex patterns for different card types
    CARD_PATTERNS = {
        'VISA': CardRegexPatterns.VISA,
        'MASTERCARD_LEGACY': CardRegexPatterns.MASTERCARD_LEGACY,
        'MASTERCARD_NEW': CardRegexPatterns.MASTERCARD_NEW
    }
    CVV_PATTERN = CardRegexPatterns.CVV
    EXPIRY_DATE_PATTERN = CardRegexPatterns.EXPIRY_DATE
    CARD_HOLDER_PATTERN = CardRegexPatterns.CARD_HOLDER

    @classmethod
    def validate_card_number(cls, card_number):
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
    def validate_card_holder_name(cls, name):
        # Validates the card holder's name (letters, spaces, hyphens, etc.)
        if not name:
            raise ValidationError(
                {'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME})

        if not re.match(cls.CARD_HOLDER_PATTERN, name):
            raise ValidationError(
                {'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME})

        return True

    @classmethod
    def validate_cvv(cls, cvv):
        # Validates the CVV (security code) for correct length and digits
        if not cvv:
            raise ValidationError({'cvv': CardErrorMessages.INVALID_CVV_CODE})

        if not re.match(cls.CVV_PATTERN, cvv):
            raise ValidationError({'cvv': CardErrorMessages.INVALID_CVV_CODE})

        return True

    @classmethod
    def validate_expiry_date(cls, expiry_date):
        # Validates the expiry date (MM/YY format) and checks if the card is expired
        if not expiry_date:
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})

        if not re.match(cls.EXPIRY_DATE_PATTERN, expiry_date):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})

        month, year = expiry_date.split('/')
        current_date = datetime.now()
        current_year = current_date.year % 100  # Get last two digits of year
        current_month = current_date.month
        exp_year = int(year)
        exp_month = int(month)

        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.CARD_HAS_EXPIRED})

        return True

    @classmethod
    def validate_payment_data(cls, payment_data):
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
    def get_user_identifier(request):
        # Uses a shared service to extract user identification info from the request
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(content_type, object_id):
        # Retrieves the product instance (inventory) for a given content type and object ID
        try:
            return content_type.get_object_for_this_type(pk=object_id)

        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    # Ensures all DB operations succeed or fail together (no partial orders)
    @transaction.atomic
    def process_order_from_shopping_bag(user, payment_data):
        # Validates payment data before processing
        PaymentValidationService.validate_payment_data(payment_data)

        shopping_bag_items = ShoppingBag.objects.filter(
            user=user
        ).select_related(
            'content_type'
        ).prefetch_related(
            'inventory'
        )

        if not shopping_bag_items.exists():
            raise ValidationError({'shopping_bag': 'Shopping bag is empty'})

        order_group = uuid.uuid4()
        orders = []

        for bag_item in shopping_bag_items:
            order = Order.objects.create(
                user=user,
                content_type=bag_item.content_type,
                object_id=bag_item.object_id,
                quantity=bag_item.quantity,
                order_group=order_group,
            )
            orders.append(order)

        shopping_bag_items.delete()

        return orders

    @staticmethod
    def get_user_orders(user):
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
    def get_user_orders_grouped(user):
        # Groups orders by order_group (all products purchased together)
        orders = OrderService.get_user_orders(user)
        grouped_orders = {}

        for order in orders:
            order_group_str = str(order.order_group)
            if order_group_str not in grouped_orders:
                grouped_orders[order_group_str] = []
            grouped_orders[order_group_str].append(order)

        return grouped_orders

    @staticmethod
    def calculate_order_group_total(order_group_id, user):
        # Calculates the total price for all orders in a group (single checkout)
        orders = Order.objects.filter(
            user=user,
            order_group=order_group_id
        ).prefetch_related('inventory')
        total = 0.0

        for order in orders:
            if order.inventory and hasattr(order.inventory, 'price'):
                total += float(order.inventory.price) * order.quantity

        return round(total, 2)
