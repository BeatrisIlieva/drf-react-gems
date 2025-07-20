from rest_framework.exceptions import ValidationError, NotFound

from src.shopping_bags.models import ShoppingBag
from src.common.services import UserIdentificationService
from src.shopping_bags.constants import ShoppingBagErrorMessages
from src.products.models.inventory import Inventory


class ShoppingBagService:
    """
    This class encapsulates all business logic related to shopping bag functionality,
    including user identification, inventory validation, and quantity management.

    Key Responsibilities:
    - User identification (authenticated vs guest users)
    - Inventory object retrieval and validation
    - Stock quantity validation
    - Atomic database operations for inventory updates
    - Shopping bag item creation and retrieval
    """

    @staticmethod
    def get_user_identifier(request):
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_inventory_object(inventory_id):
        """
        Retrieve an inventory object by its ID.
        """
        try:
            return Inventory.objects.get(pk=inventory_id)
        except Inventory.DoesNotExist:
            raise NotFound(ShoppingBagErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def validate_inventory_quantity(inventory_obj, required_quantity):
        if required_quantity > inventory_obj.quantity:
            raise ValidationError({
                'quantity': ShoppingBagErrorMessages.INSUFFICIENT_STOCK.format(quantity=inventory_obj.quantity)
            })

    @staticmethod
    def get_or_create_bag_item(filters, defaults):
        return ShoppingBag.objects.get_or_create(**filters, defaults=defaults)
