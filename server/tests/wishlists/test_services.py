# Wishlist Services Tests
# This module contains tests for the WishlistService to ensure it properly
# handles user identification, product validation, and wishlist operations.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError, NotFound
import uuid

from src.wishlists.models import Wishlist
from src.wishlists.services import WishlistService
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistServiceTestCase(TestCase):
    """
    Test case for WishlistService.
    
    This test case verifies that the WishlistService properly handles
    user identification, product validation, and wishlist operations.
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
        """
        Set up test-specific data for each test method.
        """
        # Create API client
        self.client = RequestFactory()
    
    def test_get_user_identifier_authenticated_user(self):
        """
        Test get_user_identifier with authenticated user.
        
        This test verifies that the service correctly identifies
        authenticated users and returns appropriate filter parameters.
        """
        # Arrange
        request = self.client.get('/api/wishlists/')
        request.user = self.user
        
        # Act
        user_filters = WishlistService.get_user_identifier(request)
        
        # Assert
        self.assertIn('user', user_filters)
        self.assertEqual(user_filters['user'], self.user)
        self.assertNotIn('guest_id', user_filters)
    
    def test_get_user_identifier_guest_user(self):
        """
        Test get_user_identifier with guest user.
        
        This test verifies that the service correctly identifies
        guest users and returns appropriate filter parameters.
        """
        # Arrange
        request = self.client.get('/api/wishlists/')
        request.user = AnonymousUser()
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)
        
        # Act
        user_filters = WishlistService.get_user_identifier(request)
        
        # Assert
        self.assertIn('guest_id', user_filters)
        self.assertEqual(user_filters['guest_id'], self.guest_id)
        self.assertNotIn('user', user_filters)
    
    def test_get_product_object_existing_product(self):
        """
        Test get_product_object with existing product.
        
        This test verifies that the service correctly retrieves
        product objects using ContentType framework.
        """
        # Arrange
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Act
        product_obj = WishlistService.get_product_object(content_type, object_id)
        
        # Assert
        self.assertEqual(product_obj, self.earwear)
        self.assertIsInstance(product_obj, Earwear)
        self.assertEqual(product_obj.id, self.earwear.id)
    
    def test_get_product_object_nonexistent_product(self):
        """
        Test get_product_object with nonexistent product.
        
        This test verifies that the service raises a NotFound exception
        when trying to retrieve a product that doesn't exist.
        """
        # Arrange
        content_type = self.content_type
        object_id = 99999  # Non-existent ID
        
        # Act & Assert
        with self.assertRaises(NotFound) as context:
            WishlistService.get_product_object(content_type, object_id)
        
        # Verify the error message
        from src.wishlists.constants import WishlistErrorMessages
        self.assertEqual(str(context.exception), WishlistErrorMessages.PRODUCT_NOT_FOUND)
    
    def test_check_item_exists_new_item(self):
        """
        Test check_item_exists for new item.
        
        This test verifies that the service correctly identifies
        when an item doesn't exist in the user's wishlist.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_new_item', '_new_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Act
        exists = WishlistService.check_item_exists(user_filters, content_type, object_id)
        
        # Assert
        self.assertFalse(exists)
    
    def test_check_item_exists_existing_item(self):
        """
        Test check_item_exists for existing item.
        
        This test verifies that the service correctly identifies
        when an item already exists in the user's wishlist.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_existing_item', '_existing_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Create existing wishlist item
        Wishlist.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )
        
        # Act
        exists = WishlistService.check_item_exists(user_filters, content_type, object_id)
        
        # Assert
        self.assertTrue(exists)
    
    def test_create_wishlist_item_new_item(self):
        """
        Test create_wishlist_item for new item.
        
        This test verifies that the service correctly creates
        a new wishlist item when one doesn't exist.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_create_item', '_create_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Act
        wishlist_item = WishlistService.create_wishlist_item(user_filters, content_type, object_id)
        
        # Assert
        self.assertIsInstance(wishlist_item, Wishlist)
        self.assertEqual(wishlist_item.user, user)
        self.assertEqual(wishlist_item.content_type, content_type)
        self.assertEqual(wishlist_item.object_id, object_id)
    
    def test_create_wishlist_item_duplicate_item(self):
        """
        Test create_wishlist_item for duplicate item.
        
        This test verifies that the service raises a ValidationError
        when trying to create a duplicate wishlist item.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_duplicate_item', '_duplicate_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Create existing wishlist item
        Wishlist.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )
        
        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            WishlistService.create_wishlist_item(user_filters, content_type, object_id)
        
        # Verify the error message
        from src.wishlists.constants import WishlistErrorMessages
        self.assertIn(WishlistErrorMessages.ITEM_ALREADY_EXISTS, str(context.exception))
    
    def test_get_wishlist_item_existing_item(self):
        """
        Test get_wishlist_item for existing item.
        
        This test verifies that the service correctly retrieves
        an existing wishlist item.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_get_item', '_get_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Create existing wishlist item
        existing_item = Wishlist.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )
        
        # Act
        wishlist_item = WishlistService.get_wishlist_item(user_filters, content_type, object_id)
        
        # Assert
        self.assertEqual(wishlist_item, existing_item)
        self.assertEqual(wishlist_item.user, user)
        self.assertEqual(wishlist_item.content_type, content_type)
        self.assertEqual(wishlist_item.object_id, object_id)
    
    def test_get_wishlist_item_nonexistent_item(self):
        """
        Test get_wishlist_item for nonexistent item.
        
        This test verifies that the service raises a NotFound exception
        when trying to retrieve a wishlist item that doesn't exist.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_get_nonexistent', '_get_nonexistent')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Act & Assert
        with self.assertRaises(NotFound) as context:
            WishlistService.get_wishlist_item(user_filters, content_type, object_id)
        
        # Verify the error message
        from src.wishlists.constants import WishlistErrorMessages
        self.assertEqual(str(context.exception), WishlistErrorMessages.ITEM_NOT_FOUND)
    
    def test_delete_wishlist_item_existing_item(self):
        """
        Test delete_wishlist_item for existing item.
        
        This test verifies that the service correctly deletes
        an existing wishlist item.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_delete_item', '_delete_item')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Create existing wishlist item
        existing_item = Wishlist.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )
        
        # Act
        WishlistService.delete_wishlist_item(user_filters, content_type, object_id)
        
        # Assert
        # Verify the item was deleted
        with self.assertRaises(Wishlist.DoesNotExist):
            Wishlist.objects.get(id=existing_item.id)
    
    def test_delete_wishlist_item_nonexistent_item(self):
        """
        Test delete_wishlist_item for nonexistent item.
        
        This test verifies that the service raises a NotFound exception
        when trying to delete a wishlist item that doesn't exist.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_delete_nonexistent', '_delete_nonexistent')
        user_filters = {'user': user}
        content_type = self.content_type
        object_id = self.earwear.id
        
        # Act & Assert
        with self.assertRaises(NotFound) as context:
            WishlistService.delete_wishlist_item(user_filters, content_type, object_id)
        
        # Verify the error message
        from src.wishlists.constants import WishlistErrorMessages
        self.assertEqual(str(context.exception), WishlistErrorMessages.ITEM_NOT_FOUND)
    
    def test_service_methods_static(self):
        """
        Test that service methods are static.
        
        This test verifies that the service methods can be called
        without instantiating the service class.
        """
        # Arrange
        request = self.client.get('/api/wishlists/')
        request.user = self.user
        
        # Act & Assert: All methods should be callable as static methods
        user_filters = WishlistService.get_user_identifier(request)
        self.assertIsInstance(user_filters, dict)
        
        product_obj = WishlistService.get_product_object(self.content_type, self.earwear.id)
        self.assertEqual(product_obj, self.earwear)
        
        # Should not raise exception for new item
        user = TestDataBuilder.create_authenticated_user('_static_test', '_static_test')
        user_filters = {'user': user}
        exists = WishlistService.check_item_exists(user_filters, self.content_type, self.earwear.id)
        self.assertFalse(exists) 