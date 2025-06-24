from src.shopping_bags.models import ShoppingBag


def migrate_guest_bag_to_user(user, guest_id):
    if guest_id:
        print(f"Migrating shopping bag for guest ID: {guest_id}")
        ShoppingBag.objects.filter(guest_id=guest_id, user__isnull=True).update(
            user=user, guest_id=None
        )
