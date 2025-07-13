# Accounts Utils Tests
# This module contains tests for the accounts utility functions to ensure
# guest data migration works correctly.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from src.accounts.utils import (
    migrate_guest_bag_to_user,
    migrate_guest_wishlist_to_user,
    migrate_guest_data_to_user
)
from src.shopping_bags.models import ShoppingBag
from src.wishlists.models import Wishlist
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class AccountsUtilsTestCase(TestCase):
    """
    Test case for accounts utility functions.
    
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
        cls.content_type = cls.shared_data['earwear_content_type']
    
    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create test user and guest ID
        self.user = TestDataBuilder.create_authenticated_user('_utils_test', '_utils_test')
        self.guest_id = TestDataBuilder.create_guest_id()
    
    def test_migrate_guest_bag_to_user_with_guest_id(self):
        """
        Test migrating guest shopping bag items to user.
        
        This test verifies that guest shopping bag items are
        correctly migrated to the authenticated user.
        """
        # Arrange: Create guest shopping bag items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
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
        Test migrating guest shopping bag items without guest ID.
        
        This test verifies that the function handles None guest_id
        gracefully without making any changes.
        """
        # Arrange: Create guest shopping bag items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        # Act
        migrate_guest_bag_to_user(self.user, None)
        
        # Assert: No changes should be made
        guest_bag_item.refresh_from_db()
        self.assertIsNone(guest_bag_item.user)
        self.assertEqual(guest_bag_item.guest_id, self.guest_id)
    
    def test_migrate_guest_bag_to_user_with_empty_guest_id(self):
        """
        Test migrating guest shopping bag items with empty guest ID.
        
        This test verifies that the function handles empty guest_id
        gracefully without making any changes.
        """
        # Arrange: Create guest shopping bag items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        # Act
        migrate_guest_bag_to_user(self.user, '')
        
        # Assert: No changes should be made
        guest_bag_item.refresh_from_db()
        self.assertIsNone(guest_bag_item.user)
        self.assertEqual(guest_bag_item.guest_id, self.guest_id)
    
    def test_migrate_guest_bag_to_user_multiple_items(self):
        """
        Test migrating multiple guest shopping bag items to user.
        
        This test verifies that multiple guest shopping bag items
        are correctly migrated to the authenticated user.
        """
        # Arrange: Create multiple guest shopping bag items with different products
        other_earwear = Earwear.objects.create(
            first_image='https://example.com/image3.jpg',
            second_image='https://example.com/image4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        other_inventory = Inventory.objects.create(
            quantity=5,
            price=200.00,
            size=self.size,
            content_type=self.content_type,
            object_id=other_earwear.id
        )
        
        guest_bag_item1 = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        guest_bag_item2 = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_inventory.id,
            quantity=1
        )
        
        # Act
        migrate_guest_bag_to_user(self.user, str(self.guest_id))
        
        # Assert
        guest_bag_item1.refresh_from_db()
        guest_bag_item2.refresh_from_db()
        self.assertEqual(guest_bag_item1.user, self.user)
        self.assertEqual(guest_bag_item2.user, self.user)
        self.assertIsNone(guest_bag_item1.guest_id)
        self.assertIsNone(guest_bag_item2.guest_id)
    
    def test_migrate_guest_bag_to_user_existing_user_items(self):
        """
        Test migrating guest shopping bag items when user already has items.
        
        This test verifies that guest items are migrated correctly
        even when the user already has shopping bag items.
        """
        # Arrange: Create existing user shopping bag item
        existing_item = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        # Create guest shopping bag item with different product
        other_earwear = Earwear.objects.create(
            first_image='https://example.com/image3.jpg',
            second_image='https://example.com/image4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        other_inventory = Inventory.objects.create(
            quantity=5,
            price=200.00,
            size=self.size,
            content_type=self.content_type,
            object_id=other_earwear.id
        )
        
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_inventory.id,
            quantity=2
        )
        
        # Act
        migrate_guest_bag_to_user(self.user, str(self.guest_id))
        
        # Assert
        guest_bag_item.refresh_from_db()
        self.assertEqual(guest_bag_item.user, self.user)
        self.assertIsNone(guest_bag_item.guest_id)
        # Both items should exist for the user
        self.assertEqual(ShoppingBag.objects.filter(user=self.user).count(), 2)
    
    def test_migrate_guest_wishlist_to_user_with_guest_id(self):
        """
        Test migrating guest wishlist items to user.
        
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
        Test migrating guest wishlist items without guest ID.
        
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
        Test migrating guest wishlist items with duplicates.
        
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
        
        # Create another guest wishlist item (non-duplicate)
        other_earwear = Earwear.objects.create(
            first_image='https://example.com/image3.jpg',
            second_image='https://example.com/image4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        guest_wishlist_item2 = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_earwear.id
        )
        
        # Act
        migrate_guest_wishlist_to_user(self.user, str(self.guest_id))
        
        # Assert
        # Duplicate item should be deleted
        with self.assertRaises(Wishlist.DoesNotExist):
            guest_wishlist_item.refresh_from_db()
        
        # Non-duplicate item should be migrated
        guest_wishlist_item2.refresh_from_db()
        self.assertEqual(guest_wishlist_item2.user, self.user)
        self.assertIsNone(guest_wishlist_item2.guest_id)
        
        # Original user item should still exist
        existing_item.refresh_from_db()
        self.assertEqual(existing_item.user, self.user)
    
    def test_migrate_guest_wishlist_to_user_multiple_items(self):
        """
        Test migrating multiple guest wishlist items to user.
        
        This test verifies that multiple guest wishlist items
        are correctly migrated to the authenticated user.
        """
        # Arrange: Create multiple guest wishlist items
        other_earwear1 = Earwear.objects.create(
            first_image='https://example.com/image3.jpg',
            second_image='https://example.com/image4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        other_earwear2 = Earwear.objects.create(
            first_image='https://example.com/image5.jpg',
            second_image='https://example.com/image6.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        
        guest_wishlist_item1 = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_earwear1.id
        )
        guest_wishlist_item2 = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_earwear2.id
        )
        
        # Act
        migrate_guest_wishlist_to_user(self.user, str(self.guest_id))
        
        # Assert
        guest_wishlist_item1.refresh_from_db()
        guest_wishlist_item2.refresh_from_db()
        self.assertEqual(guest_wishlist_item1.user, self.user)
        self.assertEqual(guest_wishlist_item2.user, self.user)
        self.assertIsNone(guest_wishlist_item1.guest_id)
        self.assertIsNone(guest_wishlist_item2.guest_id)
    
    def test_migrate_guest_data_to_user_comprehensive(self):
        """
        Test comprehensive guest data migration.
        
        This test verifies that both shopping bag and wishlist
        items are migrated correctly in a single operation.
        """
        # Arrange: Create guest shopping bag and wishlist items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        other_earwear = Earwear.objects.create(
            first_image='https://example.com/image3.jpg',
            second_image='https://example.com/image4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=other_earwear.id
        )
        
        # Act
        migrate_guest_data_to_user(self.user, str(self.guest_id))
        
        # Assert: Both items should be migrated
        guest_bag_item.refresh_from_db()
        guest_wishlist_item.refresh_from_db()
        
        self.assertEqual(guest_bag_item.user, self.user)
        self.assertIsNone(guest_bag_item.guest_id)
        
        self.assertEqual(guest_wishlist_item.user, self.user)
        self.assertIsNone(guest_wishlist_item.guest_id)
    
    def test_migrate_guest_data_to_user_without_guest_id(self):
        """
        Test comprehensive guest data migration without guest ID.
        
        This test verifies that the function handles None guest_id
        gracefully without making any changes.
        """
        # Arrange: Create guest shopping bag and wishlist items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )
        
        # Act
        migrate_guest_data_to_user(self.user, None)
        
        # Assert: No changes should be made
        guest_bag_item.refresh_from_db()
        guest_wishlist_item.refresh_from_db()
        
        self.assertIsNone(guest_bag_item.user)
        self.assertEqual(guest_bag_item.guest_id, self.guest_id)
        
        self.assertIsNone(guest_wishlist_item.user)
        self.assertEqual(guest_wishlist_item.guest_id, self.guest_id)
    
    def test_migrate_guest_data_to_user_empty_guest_id(self):
        """
        Test comprehensive guest data migration with empty guest ID.
        
        This test verifies that the function handles empty guest_id
        gracefully without making any changes.
        """
        # Arrange: Create guest shopping bag and wishlist items
        guest_bag_item = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )
        
        # Act
        migrate_guest_data_to_user(self.user, '')
        
        # Assert: No changes should be made
        guest_bag_item.refresh_from_db()
        guest_wishlist_item.refresh_from_db()
        
        self.assertIsNone(guest_bag_item.user)
        self.assertEqual(guest_bag_item.guest_id, self.guest_id)
        
        self.assertIsNone(guest_wishlist_item.user)
        self.assertEqual(guest_wishlist_item.guest_id, self.guest_id) 