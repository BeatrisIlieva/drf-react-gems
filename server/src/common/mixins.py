from typing import Any, Dict
from django.contrib.contenttypes.models import ContentType


class InventoryMixin:
    @staticmethod
    def get_product_info(
        obj: Any
    ) -> Dict[str, Any]:
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
    def get_total_price_per_product(
        obj: Any
    ) -> float:
        try:
            return round(obj.inventory.price * obj.quantity, 2)
        except Exception:
            return 0.0
