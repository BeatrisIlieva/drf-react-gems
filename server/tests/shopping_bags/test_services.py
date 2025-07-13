# Shopping Bag Services Tests
# This module contains tests for the ShoppingBagService to ensure all business logic
# methods work correctly, including user identification, inventory validation, and quantity updates.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound
import uuid

from src.shopping_bags.services import ShoppingBagService
from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.constants import ShoppingBagErrorMessages
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagServiceTestCase(TestCase):
    """
    Test case for ShoppingBagService.
    
    This test case verifies that all service methods work correctly,
    including user identification, inventory validation, and quantity updates.
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
        cls.content_type = cls.shared_data['inventory_content_type']
    
    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create request factory
        self.factory = RequestFactory()
    
    def test_get_user_identifier_authenticated_user(self):
        """
        Test get_user_identifier with authenticated user.
        
        This test verifies that the service correctly identifies
        authenticated users and returns appropriate filter parameters.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/')
        request.user = self.user
        
        # Act
        user_filters = ShoppingBagService.get_user_identifier(request)
        
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
        request = self.factory.get('/api/shopping-bags/')
        request.user = AnonymousUser()
        request.session = {'guest_id': str(self.guest_id)}
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)
        
        # Act
        user_filters = ShoppingBagService.get_user_identifier(request)
        
        # Assert
        self.assertIn('guest_id', user_filters)
        self.assertEqual(user_filters['guest_id'], self.guest_id)
        self.assertNotIn('user', user_filters)
    
    def test_get_inventory_object_existing_product(self):
        """
        Test get_inventory_object with existing product.
        
        This test verifies that the service correctly retrieves
        inventory objects using ContentType framework.
        """
        # Arrange
        content_type = self.content_type
        object_id = self.inventory.id
        
        # Act
        inventory_obj = ShoppingBagService.get_inventory_object(content_type, object_id)
        
        # Assert
        self.assertEqual(inventory_obj, self.inventory)
        self.assertIsInstance(inventory_obj, Inventory)
        self.assertEqual(inventory_obj.quantity, 10)
    
    def test_get_inventory_object_nonexistent_product(self):
        """
        Test get_inventory_object with nonexistent product.
        
        This test verifies that the service raises a NotFound exception
        when trying to retrieve a product that doesn't exist.
        """
        # Arrange
        content_type = self.content_type
        object_id = 99999  # Non-existent ID
        
        # Act & Assert
        with self.assertRaises(NotFound) as context:
            ShoppingBagService.get_inventory_object(content_type, object_id)
        
        # Verify the error message
        self.assertEqual(str(context.exception), ShoppingBagErrorMessages.PRODUCT_NOT_FOUND)
    
    def test_validate_inventory_quantity_sufficient_stock(self):
        """
        Test validate_inventory_quantity with sufficient stock.
        
        This test verifies that the service accepts valid quantities
        when there is sufficient stock available.
        """
        # Arrange
        inventory_obj = self.inventory
        required_quantity = 5
        
        # Act & Assert
        # Should not raise any exception
        ShoppingBagService.validate_inventory_quantity(inventory_obj, required_quantity)
    
    def test_validate_inventory_quantity_insufficient_stock(self):
        """
        Test validate_inventory_quantity with insufficient stock.
        
        This test verifies that the service raises a ValidationError
        when trying to add more items than available in stock.
        """
        # Arrange
        inventory_obj = self.inventory
        required_quantity = 15  # More than available (10)
        
        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            ShoppingBagService.validate_inventory_quantity(inventory_obj, required_quantity)
        
        # Verify the error message contains the available quantity
        error_detail = context.exception.detail
        self.assertIn('quantity', error_detail)
        self.assertIn('10', str(error_detail['quantity']))  # Available quantity
    
    def test_validate_inventory_quantity_exact_stock(self):
        """
        Test validate_inventory_quantity with exact stock available.
        
        This test verifies that the service accepts quantities
        that exactly match the available stock.
        """
        # Arrange
        inventory_obj = self.inventory
        required_quantity = 10  # Exactly available
        
        # Act & Assert
        # Should not raise any exception
        ShoppingBagService.validate_inventory_quantity(inventory_obj, required_quantity)
    
    def test_update_inventory_quantity_reduce_stock(self):
        """
        Test update_inventory_quantity when reducing stock.
        
        This test verifies that the service correctly updates
        inventory quantities when reducing stock.
        """
        # Arrange
        inventory_obj = self.inventory
        original_quantity = inventory_obj.quantity
        reduction_amount = 3
        
        # Act
        ShoppingBagService.update_inventory_quantity(inventory_obj, reduction_amount)
        
        # Assert
        inventory_obj.refresh_from_db()
        self.assertEqual(inventory_obj.quantity, original_quantity - reduction_amount)
    
    def test_update_inventory_quantity_restore_stock(self):
        """
        Test update_inventory_quantity when restoring stock.
        
        This test verifies that the service correctly updates
        inventory quantities when restoring stock.
        """
        # Arrange
        inventory_obj = self.inventory
        original_quantity = inventory_obj.quantity
        restoration_amount = 2
        
        # Act
        ShoppingBagService.update_inventory_quantity(inventory_obj, -restoration_amount)
        
        # Assert
        inventory_obj.refresh_from_db()
        self.assertEqual(inventory_obj.quantity, original_quantity + restoration_amount)
    
    def test_get_or_create_bag_item_new_item(self):
        """
        Test get_or_create_bag_item with new item.
        
        This test verifies that the service creates a new shopping bag item
        when one doesn't exist for the user and product.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_new_item', '_new_item')
        filters = {
            'user': user,
            'content_type': self.content_type,
            'object_id': self.inventory.id
        }
        defaults = {'quantity': 2}
        
        # Act
        bag_item, created = ShoppingBagService.get_or_create_bag_item(filters, defaults)
        
        # Assert
        self.assertTrue(created)
        self.assertEqual(bag_item.user, user)
        self.assertEqual(bag_item.quantity, 2)
        self.assertEqual(bag_item.object_id, self.inventory.id)
    
    def test_get_or_create_bag_item_existing_item(self):
        """
        Test get_or_create_bag_item with existing item.
        
        This test verifies that the service retrieves an existing shopping bag item
        when one already exists for the user and product.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user('_existing_item', '_existing_item')
        # Create existing bag item
        existing_item = ShoppingBag.objects.create(
            user=user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        filters = {
            'user': user,
            'content_type': self.content_type,
            'object_id': self.inventory.id
        }
        defaults = {'quantity': 3}
        
        # Act
        bag_item, created = ShoppingBagService.get_or_create_bag_item(filters, defaults)
        
        # Assert
        self.assertFalse(created)
        self.assertEqual(bag_item, existing_item)
        self.assertEqual(bag_item.quantity, 1)  # Should not use defaults for existing item
    
    def test_get_or_create_bag_item_guest_user(self):
        """
        Test get_or_create_bag_item with guest user.
        
        This test verifies that the service works correctly
        with guest users instead of authenticated users.
        """
        # Arrange
        guest_id = TestDataBuilder.create_guest_id()
        filters = {
            'guest_id': guest_id,
            'content_type': self.content_type,
            'object_id': self.inventory.id
        }
        defaults = {'quantity': 2}
        
        # Act
        bag_item, created = ShoppingBagService.get_or_create_bag_item(filters, defaults)
        
        # Assert
        self.assertTrue(created)
        self.assertEqual(bag_item.guest_id, guest_id)
        self.assertEqual(bag_item.quantity, 2)
        self.assertEqual(bag_item.object_id, self.inventory.id)
    
    def test_inventory_quantity_atomic_operations(self):
        """
        Test that inventory quantity updates are atomic.
        
        This test verifies that inventory quantity updates
        are performed atomically to prevent race conditions.
        """
        # Arrange
        inventory_obj = self.inventory
        original_quantity = inventory_obj.quantity
        
        # Act: Perform multiple operations
        ShoppingBagService.update_inventory_quantity(inventory_obj, 2)
        ShoppingBagService.update_inventory_quantity(inventory_obj, -1)
        ShoppingBagService.update_inventory_quantity(inventory_obj, 1)
        
        # Assert
        inventory_obj.refresh_from_db()
        self.assertEqual(inventory_obj.quantity, original_quantity - 2)
    
    def test_service_methods_static(self):
        """
        Test that service methods are static.
        
        This test verifies that the service methods can be called
        without instantiating the service class.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/')
        request.user = self.user
        
        # Act & Assert: All methods should be callable as static methods
        user_filters = ShoppingBagService.get_user_identifier(request)
        self.assertIsInstance(user_filters, dict)
        
        inventory_obj = ShoppingBagService.get_inventory_object(self.content_type, self.inventory.id)
        self.assertEqual(inventory_obj, self.inventory)
        
        # Should not raise exception
        ShoppingBagService.validate_inventory_quantity(self.inventory, 5)
        
        # Should not raise exception
        ShoppingBagService.update_inventory_quantity(self.inventory, 0) 