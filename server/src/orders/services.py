from django.db import transaction
from django.db.models import QuerySet
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError, NotFound

from typing import Dict, Any, List
from datetime import datetime
import re
import uuid

from src.orders.models import Order
from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService
from src.orders.constants import CardErrorMessages, CardRegexPatterns


class PaymentValidationService:
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
        if not expiry_date:
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})
        if not re.match(cls.EXPIRY_DATE_PATTERN, expiry_date):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.INVALID_EXPIRY_DATE})
        month, year = expiry_date.split('/')
        current_date = datetime.now()
        current_year = current_date.year % 100
        current_month = current_date.month
        exp_year = int(year)
        exp_month = int(month)
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            raise ValidationError(
                {'expiry_date': CardErrorMessages.CARD_HAS_EXPIRED})
        return True

    @classmethod
    def validate_payment_data(
        cls,
        payment_data: Dict[str, str]
    ) -> bool:
        cls.validate_card_number(payment_data.get('card_number'))
        cls.validate_card_holder_name(payment_data.get('card_holder_name'))
        cls.validate_cvv(payment_data.get('cvv'))
        cls.validate_expiry_date(payment_data.get('expiry_date'))
        return True


class OrderService:
    @staticmethod
    def get_user_identifier(
        request: Any
    ) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(
        content_type: ContentType,
        object_id: int
    ) -> Any:
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    @transaction.atomic
    def process_order_from_shopping_bag(
        user: Any,
        payment_data: Dict[str, str]
    ) -> List[Order]:
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
        orders: List[Order] = []
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
    def get_user_orders(
        user: Any
    ) -> QuerySet[Order]:
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
        orders = Order.objects.filter(
            user=user,
            order_group=order_group_id
        ).prefetch_related('inventory')
        total: float = 0.0
        for order in orders:
            if order.inventory and hasattr(order.inventory, 'price'):
                total += float(order.inventory.price) * order.quantity
        return round(total, 2)
