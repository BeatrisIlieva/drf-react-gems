from src.shopping_bags.models import ShoppingBag
from src.wishlists.models import Wishlist


def migrate_guest_bag_to_user(user, guest_id):
    if guest_id:
        ShoppingBag.objects.filter(
            guest_id=guest_id, user__isnull=True
        ).update(
            user=user, guest_id=None
        )


def migrate_guest_wishlist_to_user(user, guest_id):
    if guest_id:
        # Get all guest wishlist items
        guest_wishlist_items = Wishlist.objects.filter(
            guest_id=guest_id, user__isnull=True
        )

        # Check for duplicates and migrate non-duplicate items
        migrated_count = 0
        for item in guest_wishlist_items:
            # Check if user already has this item in their wishlist
            existing_item = Wishlist.objects.filter(
                user=user,
                content_type=item.content_type,
                object_id=item.object_id,
            ).exists()

            if not existing_item:
                # Migrate the item
                item.user = user
                item.guest_id = None
                item.save()
                migrated_count += 1
            else:
                # Delete the duplicate guest item
                item.delete()

        print(f'Migrated {migrated_count} wishlist items to user {user.email}')


def migrate_guest_data_to_user(user, guest_id):
    if guest_id:
        migrate_guest_bag_to_user(user, guest_id)
        migrate_guest_wishlist_to_user(user, guest_id)
