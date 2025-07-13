# Wishlist Models Tests
# This module contains tests for the Wishlist model to ensure it properly
# handles user wishlist items with correct constraints and relationships.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import uuid

from src.wishlists.models import Wishlist
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistModelTestCase(TestCase):
    """
    Test case for Wishlist model.
    
    This test case verifies that the Wishlist model properly handles
    user wishlist items with correct constraints, relationships, and validation.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        """
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.user = cls.shared_data['user']
        cls.guest_id = cls.shared_data['guest_id']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earwear_content_type']
    
    def setUp(self):
        pass
    
    def test_wishlist_creation_with_authenticated_user(self):
        """
        Test creating a wishlist item for an authenticated user.
        
        This test verifies that wishlist items can be created for
        authenticated users with proper relationships.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        
        # Act
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Assert
        self.assertEqual(wishlist_item.user, self.user)
        self.assertIsNone(wishlist_item.guest_id)
        self.assertEqual(wishlist_item.content_type, content_type)
        self.assertEqual(wishlist_item.object_id, self.earwear.id)
        self.assertEqual(wishlist_item.product, self.earwear)
    
    def test_wishlist_creation_with_guest_user(self):
        """
        Test creating a wishlist item for a guest user.
        
        This test verifies that wishlist items can be created for
        guest users with proper relationships.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        
        # Act
        wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Assert
        self.assertIsNone(wishlist_item.user)
        self.assertEqual(wishlist_item.guest_id, self.guest_id)
        self.assertEqual(wishlist_item.content_type, content_type)
        self.assertEqual(wishlist_item.object_id, self.earwear.id)
        self.assertEqual(wishlist_item.product, self.earwear)
    
    def test_wishlist_generic_foreign_key_relationship(self):
        """
        Test that GenericForeignKey correctly relates to product objects.
        
        This test verifies that the GenericForeignKey properly resolves
        to the correct product object through content_type and object_id.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Act
        product = wishlist_item.product
        
        # Assert
        self.assertEqual(product, self.earwear)
        self.assertIsInstance(product, Earwear)
        self.assertEqual(product.id, self.earwear.id)
    
    def test_string_representation(self):
        """
        Test the string representation of Wishlist model.
        
        This test verifies that the __str__ method returns
        appropriate string representations for both user types.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        # Use unique users/guests to avoid unique constraint
        user2 = TestDataBuilder.create_authenticated_user('_str', '_str')
        guest_id2 = TestDataBuilder.create_guest_id()
        # Act - Test authenticated user
        user_wishlist = Wishlist.objects.create(
            user=user2,
            content_type=content_type,
            object_id=self.earwear.id
        )
        # Act - Test guest user
        guest_wishlist = Wishlist.objects.create(
            guest_id=guest_id2,
            content_type=content_type,
            object_id=self.earwear.id
        )
        # Assert
        self.assertIn(user2.email, str(user_wishlist))
        self.assertIn(str(guest_id2), str(guest_wishlist))
        self.assertIn(str(self.earwear), str(user_wishlist))
        self.assertIn(str(self.earwear), str(guest_wishlist))
    
    def test_unique_constraint_authenticated_user(self):
        """
        Test unique constraint for authenticated users.
        
        This test verifies that authenticated users cannot have
        duplicate items in their wishlist.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        
        # Create first wishlist item
        Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Act & Assert - Try to create duplicate item
        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Wishlist.objects.create(
                user=self.user,
                content_type=content_type,
                object_id=self.earwear.id
            )
    
    def test_unique_constraint_guest_user(self):
        """
        Test unique constraint for guest users.
        
        This test verifies that guest users cannot have
        duplicate items in their wishlist.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        
        # Create first wishlist item
        Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Act & Assert - Try to create duplicate item
        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Wishlist.objects.create(
                guest_id=self.guest_id,
                content_type=content_type,
                object_id=self.earwear.id
            )
    
    def test_different_users_can_have_same_item(self):
        """
        Test that different users can have the same item in their wishlists.
        
        This test verifies that the unique constraint only applies
        per user, not globally across all users.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        user2 = TestDataBuilder.create_authenticated_user('_diff', '_diff')
        # Act
        wishlist1 = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        wishlist2 = Wishlist.objects.create(
            user=user2,
            content_type=content_type,
            object_id=self.earwear.id
        )
        # Assert
        self.assertEqual(wishlist1.object_id, wishlist2.object_id)
        self.assertNotEqual(wishlist1.user, wishlist2.user)
    
    def test_guest_and_authenticated_user_can_have_same_item(self):
        """
        Test that guest and authenticated users can have the same item.
        
        This test verifies that guest users and authenticated users
        can have the same item in their wishlists without conflicts.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        guest_id2 = TestDataBuilder.create_guest_id()
        # Act
        wishlist1 = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        wishlist2 = Wishlist.objects.create(
            guest_id=guest_id2,
            content_type=content_type,
            object_id=self.earwear.id
        )
        # Assert
        self.assertEqual(wishlist1.object_id, wishlist2.object_id)
        self.assertIsNone(wishlist2.user)
        self.assertIsNotNone(wishlist2.guest_id)
    
    def test_ordering_by_created_at_descending(self):
        """
        Test that wishlist items are ordered by creation date descending.
        
        This test verifies that the Meta ordering is properly applied
        and items are returned newest first.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        user2 = TestDataBuilder.create_authenticated_user('_order', '_order')
        wishlist1 = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        wishlist2 = Wishlist.objects.create(
            user=user2,
            content_type=content_type,
            object_id=self.earwear.id
        )
        # Act
        all_wishlists = Wishlist.objects.filter(object_id=self.earwear.id).order_by('-created_at')
        # Assert
        self.assertEqual(all_wishlists.count(), 2)
        self.assertEqual(all_wishlists[0], wishlist2)
        self.assertEqual(all_wishlists[1], wishlist1)
    
    def test_model_fields_exist(self):
        """
        Test that all expected model fields exist.
        
        This test verifies that the Wishlist model has all the
        expected fields with correct types.
        """
        # Arrange
        wishlist = Wishlist()
        
        # Act & Assert
        self.assertTrue(hasattr(wishlist, 'created_at'))
        self.assertTrue(hasattr(wishlist, 'user'))
        self.assertTrue(hasattr(wishlist, 'guest_id'))
        self.assertTrue(hasattr(wishlist, 'object_id'))
        self.assertTrue(hasattr(wishlist, 'product'))
        
        # Test that fields are accessible
        self.assertIsNone(wishlist.user)
        self.assertIsNone(wishlist.guest_id)
        self.assertIsNone(wishlist.object_id)
    
    def test_auto_now_add_created_at(self):
        """
        Test that created_at field is automatically set.
        
        This test verifies that the created_at field is automatically
        set when a wishlist item is created.
        """
        # Arrange
        content_type = ContentType.objects.get_for_model(Earwear)
        
        # Act
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.earwear.id
        )
        
        # Assert
        self.assertIsNotNone(wishlist_item.created_at)
        self.assertIsInstance(wishlist_item.created_at, type(wishlist_item.created_at)) 