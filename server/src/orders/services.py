from django.db import transaction

from rest_framework.exceptions import ValidationError

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
        'MASTERCARD_NEW': CardRegexPatterns.MASTERCARD_NEW,
    }
    CVV_PATTERN = CardRegexPatterns.CVV
    EXPIRY_DATE_PATTERN = CardRegexPatterns.EXPIRY_DATE
    CARD_HOLDER_PATTERN = CardRegexPatterns.CARD_HOLDER

    @classmethod
    def validate_card_number(cls, card_number):
        # Validates the card number using regex patterns for supported card types
        if not card_number:
            raise ValidationError(
                {
                    'card_number': CardErrorMessages.INVALID_CARD_NUMBER,
                }
            )

        for pattern in cls.CARD_PATTERNS.values():
            if re.match(pattern, card_number):
                return True

        raise ValidationError(
            {
                'card_number': CardErrorMessages.INVALID_CARD_NUMBER,
            }
        )

    @classmethod
    def validate_card_holder_name(cls, name):
        # Validates the card holder's name (letters, spaces, hyphens, etc.)
        if not name:
            raise ValidationError(
                {
                    'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME,
                }
            )

        if not re.match(cls.CARD_HOLDER_PATTERN, name):
            raise ValidationError(
                {
                    'card_holder_name': CardErrorMessages.INVALID_CARD_HOLDER_NAME
                }
            )

        return True

    @classmethod
    def validate_cvv(cls, cvv):
        # Validates the CVV (security code) for correct length and digits
        if not cvv:
            raise ValidationError(
                {
                    'cvv': CardErrorMessages.INVALID_CVV_CODE,
                }
            )

        if not re.match(cls.CVV_PATTERN, cvv):
            raise ValidationError(
                {
                    'cvv': CardErrorMessages.INVALID_CVV_CODE,
                }
            )

        return True

    @classmethod
    def validate_expiry_date(cls, expiry_date):
        # Validates the expiry date (MM/YY format) and checks if the card is expired
        if not expiry_date:
            raise ValidationError(
                {
                    'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE,
                }
            )

        if not re.match(cls.EXPIRY_DATE_PATTERN, expiry_date):
            raise ValidationError(
                {
                    'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE,
                }
            )

        month, year = expiry_date.split('/')
        current_date = datetime.now()
        current_year = current_date.year % 100  # Get last two digits of year
        current_month = current_date.month
        exp_year = int(year)
        exp_month = int(month)

        if exp_year < current_year or (
            exp_year == current_year and exp_month < current_month
        ):
            raise ValidationError(
                {
                    'expiry_date': CardErrorMessages.CARD_HAS_EXPIRED,
                }
            )

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
    @transaction.atomic
    def process_order_from_shopping_bag(user):
        shopping_bag_items = ShoppingBag.objects.filter(
            user=user
        ).select_related('inventory')

        if not shopping_bag_items.exists():
            raise ValidationError(
                {
                    'shopping_bag': 'Shopping bag is empty',
                }
            )

        order_group = uuid.uuid4()
        orders = []

        for bag_item in shopping_bag_items:
            order = Order.objects.create(
                user=user,
                inventory=bag_item.inventory,
                quantity=bag_item.quantity,
                order_group=order_group,
            )
            orders.append(order)

        shopping_bag_items.delete()

        return orders

    @staticmethod
    def get_user_orders(user):
        # Retrieves all orders for a user, with related product and user info
        return (
            Order.objects.filter(
                user=user,
            )
            .select_related(
                'inventory',
                'user',
            )
            .order_by(
                '-created_at',
            )
        )

    @staticmethod
    def get_user_orders_grouped(user):
        """
        Groups orders by order_group, but only includes one entry per unique product (not per inventory/size).
        The order group total is still calculated as the sum of all order items in the group.
        Do not modify the order objects (do not set quantity to None).
        """
        orders = OrderService.get_user_orders(user)
        grouped_orders = {}

        for order in orders:
            order_group_str = str(order.order_group)
            if order_group_str not in grouped_orders:
                grouped_orders[order_group_str] = {}
            # Use (product_content_type, product_object_id) as the unique key

            inventory = order.inventory

            product = getattr(inventory, 'product', None)
            if not product:
                continue

            product_key = (product._meta.model_name, product.id)
            if product_key not in grouped_orders[order_group_str]:
                grouped_orders[order_group_str][product_key] = order

        # Convert dicts to lists for serializer compatibility
        for group in grouped_orders:
            grouped_orders[group] = list(grouped_orders[group].values())

        return grouped_orders

    @staticmethod
    def calculate_order_group_total(order_group_id, user):
        # Calculates the total price for all orders in a group (single checkout)
        orders = Order.objects.filter(
            user=user,
            order_group=order_group_id,
        ).select_related('inventory')

        total = 0.0

        for order in orders:
            if order.inventory and hasattr(order.inventory, 'price'):
                total += float(order.inventory.price) * order.quantity

        return round(total, 2)
