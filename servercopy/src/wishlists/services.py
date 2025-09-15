from rest_framework.exceptions import ValidationError, NotFound

from src.wishlists.models import Wishlist
from src.common.services import UserIdentificationService
from src.wishlists.constants import WishlistErrorMessages


class WishlistService:
    @staticmethod
    def get_user_identifier(request):
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_product_object(content_type, object_id):
        """
        Retrieve a product object using ContentType framework.

        This method validates that the requested product exists in the database
        and returns the actual product object for further operations.
        """
        try:
            return content_type.get_object_for_this_type(pk=object_id)

        except content_type.model_class().DoesNotExist:
            raise NotFound(WishlistErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def check_item_exists(user_filters, content_type, object_id):
        """
        Check if a wishlist item already exists for the user.

        This method prevents duplicate items in the wishlist by checking
        if the user already has the specific
        product in their wishlist.
        """
        return Wishlist.objects.filter(
            content_type=content_type,
            object_id=object_id,
            **user_filters,
        ).exists()

    @staticmethod
    def create_wishlist_item(user_filters, content_type, object_id):
        """
        This method creates a new wishlist item after validating that:
        1. The product exists in the database
        2. The user doesn't already have this item in their wishlist
        """
        # Check if item already exists to prevent duplicates
        if WishlistService.check_item_exists(
            user_filters,
            content_type,
            object_id,
        ):
            raise ValidationError(
                {
                    'detail': WishlistErrorMessages.ITEM_ALREADY_EXISTS,
                }
            )

        # Validate that the product exists
        WishlistService.get_product_object(content_type, object_id)

        # Create the wishlist item
        created_item = Wishlist.objects.create(
            content_type=content_type,
            object_id=object_id,
            **user_filters,
        )

        return created_item

    @staticmethod
    def get_wishlist_item(user_filters, content_type, object_id):
        """
        This method finds and returns a specific wishlist item for the user
        and the specified product.
        """
        try:
            item = Wishlist.objects.get(
                content_type=content_type,
                object_id=object_id,
                **user_filters,
            )
            return item

        except Wishlist.DoesNotExist:
            raise NotFound(WishlistErrorMessages.ITEM_NOT_FOUND)

    @staticmethod
    def delete_wishlist_item(user_filters, content_type, object_id):
        """
        This method removes a specific wishlist item from the user's wishlist.
        It first validates that the item exists before deletion.
        """
        # Get the wishlist item (this will raise NotFound if it doesn't exist)
        wishlist_item = WishlistService.get_wishlist_item(
            user_filters,
            content_type,
            object_id,
        )

        # Delete the item
        wishlist_item.delete()

        return True
