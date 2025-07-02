from django.core.validators import EmailValidator
from src.shopping_bags.models import ShoppingBag
from src.wishlists.models import Wishlist
from src.accounts.validators.models import UsernameValidator, EmailOrUsernameValidator
import re


def migrate_guest_bag_to_user(user, guest_id):
    if guest_id:
        print(f"Migrating shopping bag for guest ID: {guest_id}")
        ShoppingBag.objects.filter(guest_id=guest_id, user__isnull=True).update(
            user=user, guest_id=None
        )


def migrate_guest_wishlist_to_user(user, guest_id):
    """Migrate guest wishlist items to authenticated user"""
    if guest_id:
        print(f"Migrating wishlist for guest ID: {guest_id}")

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

        print(f"Migrated {migrated_count} wishlist items to user {user.email}")


def migrate_guest_data_to_user(user, guest_id):
    """Migrate all guest data (shopping bag and wishlist) to authenticated user"""
    if guest_id:
        migrate_guest_bag_to_user(user, guest_id)
        migrate_guest_wishlist_to_user(user, guest_id)


def is_valid_email(email):
    """
    Check if a string is a valid email address
    Returns True if valid, False otherwise
    """
    try:
        validator = EmailValidator()
        validator(email)
        return True
    except:
        return False


def is_valid_username(username):
    """
    Check if a string is a valid username
    Returns True if valid, False otherwise
    """
    try:
        validator = UsernameValidator()
        validator(username)
        return True
    except:
        return False


def is_valid_email_or_username(value):
    """
    Check if a string is either a valid email or username
    Returns True if valid, False otherwise
    """
    try:
        validator = EmailOrUsernameValidator()
        validator(value)
        return True
    except:
        return False


def get_credential_type(value):
    """
    Determine if a credential is an email or username
    Returns 'email', 'username', or 'invalid'
    """
    if is_valid_email(value):
        return 'email'
    elif is_valid_username(value):
        return 'username'
    else:
        return 'invalid'
