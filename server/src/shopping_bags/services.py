from django.db import transaction
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
from typing import Dict, Any

from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService


class ShoppingBagService:
    @staticmethod
    def get_user_identifier(request) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(content_type: ContentType, object_id: int):
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    def validate_inventory_quantity(inventory_obj, required_quantity: int):
        if required_quantity > inventory_obj.quantity:
            raise ValidationError({
                'quantity': f'Only {inventory_obj.quantity} items available in stock'
            })

    @staticmethod
    @transaction.atomic
    def update_inventory_quantity(inventory_obj, delta: int):
        inventory_obj.quantity = F('quantity') - delta
        inventory_obj.save(update_fields=['quantity'])
        inventory_obj.refresh_from_db()

    @staticmethod
    def get_or_create_bag_item(filters: Dict[str, Any], defaults: Dict[str, Any]):
        return ShoppingBag.objects.get_or_create(**filters, defaults=defaults)
