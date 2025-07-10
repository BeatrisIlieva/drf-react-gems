from django.db import transaction
from django.db.models import F
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError, NotFound

from typing import Dict, Any
from django.http import HttpRequest

from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService
from src.shopping_bags.constants import ShoppingBagErrorMessages


class ShoppingBagService:
    @staticmethod
    def get_user_identifier(request: HttpRequest) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(content_type: ContentType, object_id: int) -> Any:
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound(ShoppingBagErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def validate_inventory_quantity(inventory_obj: Any, required_quantity: int) -> None:
        if required_quantity > inventory_obj.quantity:
            raise ValidationError({
                'quantity': ShoppingBagErrorMessages.INSUFFICIENT_STOCK.format(quantity=inventory_obj.quantity)
            })

    @staticmethod
    @transaction.atomic
    def update_inventory_quantity(inventory_obj: Any, delta: int) -> None:
        inventory_obj.quantity = F('quantity') - delta
        inventory_obj.save(update_fields=['quantity'])
        inventory_obj.refresh_from_db()

    @staticmethod
    def get_or_create_bag_item(filters: Dict[str, Any], defaults: Dict[str, Any]) -> tuple[ShoppingBag, bool]:
        return ShoppingBag.objects.get_or_create(**filters, defaults=defaults)
