from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
from typing import Dict, Any

from src.wishlists.models import Wishlist
from src.common.services import UserIdentificationService


class WishlistService:
    @staticmethod
    def get_user_identifier(request) -> Dict[str, Any]:
        return UserIdentificationService.get_user_identifier(request)

    @staticmethod
    def get_product_object(content_type: ContentType, object_id: int):
        try:
            return content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise NotFound('Product not found')

    @staticmethod
    def check_item_exists(user_filters: Dict[str, Any], content_type: ContentType, object_id: int) -> bool:
        return Wishlist.objects.filter(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        ).exists()

    @staticmethod
    def create_wishlist_item(user_filters: Dict[str, Any], content_type: ContentType, object_id: int):
        if WishlistService.check_item_exists(user_filters, content_type, object_id):
            raise ValidationError({'detail': 'Item already in wishlist'})

        WishlistService.get_product_object(content_type, object_id)

        created_item = Wishlist.objects.create(
            content_type=content_type,
            object_id=object_id,
            **user_filters
        )
        
        return created_item

    @staticmethod
    def get_wishlist_item(user_filters: Dict[str, Any], content_type: ContentType, object_id: int):
        print(f"DEBUG: Looking for wishlist item with filters: {user_filters}, content_type: {content_type}, object_id: {object_id}")
        try:
            item = Wishlist.objects.get(
                content_type=content_type,
                object_id=object_id,
                **user_filters
            )
            print(f"DEBUG: Found wishlist item: {item.id}")
            return item
        except Wishlist.DoesNotExist:
            print(f"DEBUG: Wishlist item not found")
            # Let's see what items exist for this content_type and object_id
            all_items = Wishlist.objects.filter(content_type=content_type, object_id=object_id)
            print(f"DEBUG: All items for this content_type/object_id: {[(item.id, item.user, item.guest_id) for item in all_items]}")
            raise NotFound('Wishlist item not found')

    @staticmethod
    def delete_wishlist_item(user_filters: Dict[str, Any], content_type: ContentType, object_id: int):
        wishlist_item = WishlistService.get_wishlist_item(
            user_filters, content_type, object_id)
        wishlist_item.delete()
        return True
