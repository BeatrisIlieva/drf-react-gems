from django.test import TestCase
from django.contrib.auth import get_user_model

from src.accounts.utils import (
    migrate_guest_bag_to_user,
    migrate_guest_wishlist_to_user,
)
from src.shopping_bags.models import ShoppingBag
from src.wishlists.models import Wishlist
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class AccountsUtilsTestCase(TestCase):
    """
    This test case verifies that guest data migration functions
    work correctly for shopping bags and wishlists.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        """
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['inventory_content_type']

    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create test user and guest ID
        self.user = TestDataBuilder.create_authenticated_user(
            '_utils_test', '_utils_test')
        self.guest_id = TestDataBuilder.create_guest_id()

    def test_migrate_guest_bag_to_user_with_guest_id(self):
        """
        This test verifies that guest shopping bag items are
        correctly migrated to the authenticated user.
        """
        # Arrange
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            inventory=self.inventory,
            quantity=2
        )

        # Act
        migrate_guest_bag_to_user(self.user, str(self.guest_id))

        # Assert
        guest_bag_item.refresh_from_db()
        self.assertEqual(guest_bag_item.user, self.user)
        self.assertIsNone(guest_bag_item.guest_id)
        self.assertEqual(guest_bag_item.quantity, 2)

    def test_migrate_guest_bag_to_user_without_guest_id(self):
        """
        This test verifies that the function handles None guest_id.
        """
        # Arrange: Create guest shopping bag items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            inventory=self.inventory,
            quantity=2
        )

        # Act
        migrate_guest_bag_to_user(self.user, None)

        # Assert: No changes should be made
        guest_bag_item.refresh_from_db()
        self.assertIsNone(guest_bag_item.user)
        self.assertEqual(guest_bag_item.guest_id, self.guest_id)

    def test_migrate_guest_wishlist_to_user_with_guest_id(self):
        """
        This test verifies that guest wishlist items are
        correctly migrated to the authenticated user.
        """
        # Arrange: Create guest wishlist item
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        # Act
        migrate_guest_wishlist_to_user(self.user, str(self.guest_id))

        # Assert
        guest_wishlist_item.refresh_from_db()
        self.assertEqual(guest_wishlist_item.user, self.user)
        self.assertIsNone(guest_wishlist_item.guest_id)

    def test_migrate_guest_wishlist_to_user_without_guest_id(self):
        """
        This test verifies that the function handles None guest_id
        gracefully without making any changes.
        """
        # Arrange: Create guest wishlist item
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        # Act
        migrate_guest_wishlist_to_user(self.user, None)

        # Assert: No changes should be made
        guest_wishlist_item.refresh_from_db()
        self.assertIsNone(guest_wishlist_item.user)
        self.assertEqual(guest_wishlist_item.guest_id, self.guest_id)

    def test_migrate_guest_wishlist_to_user_duplicate_items(self):
        """
        This test verifies that duplicate items are handled correctly:
        - Non-duplicate items are migrated
        - Duplicate items are deleted
        """
        # Arrange: Create existing user wishlist item
        existing_item = Wishlist.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        # Create guest wishlist item (duplicate)
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        # Act
        migrate_guest_wishlist_to_user(self.user, str(self.guest_id))

        # Assert
        # Duplicate item should be deleted
        with self.assertRaises(Wishlist.DoesNotExist):
            guest_wishlist_item.refresh_from_db()

        # Original user item should still exist
        existing_item.refresh_from_db()
        self.assertEqual(existing_item.user, self.user)
