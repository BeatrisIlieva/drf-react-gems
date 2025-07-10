from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
from typing import Dict, Any

from src.wishlists.models import Wishlist
from src.common.services import UserIdentificationService
from src.wishlists.constants import WishlistErrorMessages


class WishlistService:
    @staticmethod
    def get_user_identifier(
        request: Any
    ) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_product_object(
        content_type: ContentType,
        object_id: int
    ) -> Any:
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound(WishlistErrorMessages.PRODUCT_NOT_FOUND)

    @staticmethod
    def check_item_exists(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> bool:
        return Wishlist.objects.filter(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        ).exists()

    @staticmethod
    def create_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> Wishlist:
        if WishlistService.check_item_exists(user_filters, content_type, object_id):
            raise ValidationError({'detail': WishlistErrorMessages.ITEM_ALREADY_EXISTS})
        WishlistService.get_product_object(content_type, object_id)
        created_item: Wishlist = Wishlist.objects.create(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        )
        return created_item

    @staticmethod
    def get_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> Wishlist:
        try:
            item: Wishlist = Wishlist.objects.get(
                content_type=content_type,
                object_id=object_id,
                **user_filters
            )
            return item
        except Wishlist.DoesNotExist:
            raise NotFound(WishlistErrorMessages.ITEM_NOT_FOUND)

    @staticmethod
    def delete_wishlist_item(
        user_filters: Dict[str, Any],
        content_type: ContentType,
        object_id: int
    ) -> bool:
        wishlist_item: Wishlist = WishlistService.get_wishlist_item(
            user_filters, content_type, object_id
        )
        wishlist_item.delete()
        return True
