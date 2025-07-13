# Shopping Bag Serializers Tests
# This module contains tests for the ShoppingBagSerializer to ensure it properly
# serializes and deserializes shopping bag data with computed fields.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import uuid
import unittest

from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.serializers import ShoppingBagSerializer
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagSerializerTestCase(TestCase):
    """
    Test case for ShoppingBagSerializer.
    
    This test case verifies that the ShoppingBagSerializer properly handles
    serialization and deserialization of shopping bag data, including
    computed fields for product information and total price.
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
        
        # Create test shopping bag item
        cls.shopping_bag = ShoppingBag.objects.create(
            user=cls.user,
            content_type=cls.content_type,
            object_id=cls.inventory.id,
            quantity=2
        )
    
    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        pass
    
    def test_serializer_fields(self):
        """
        Test that serializer includes all expected fields.
        
        This test verifies that the serializer includes all the fields
        defined in the Meta class and that they are properly configured.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        data = serializer.data
        
        # Assert
        expected_fields = [
            'id', 'user', 'quantity', 'created_at', 'content_type',
            'object_id', 'product_info', 'total_price'
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_serializer_read_only_fields(self):
        """
        Test that read-only fields cannot be modified.
        
        This test verifies that the read-only fields are properly configured
        and cannot be modified through the serializer.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        read_only_fields = serializer.Meta.read_only_fields
        
        # Assert
        expected_read_only_fields = [
            'id', 'created_at', 'user', 'product_info', 'total_price'
        ]
        
        for field in expected_read_only_fields:
            self.assertIn(field, read_only_fields)
    
    def test_serializer_content_type_field(self):
        """
        Test that content_type field uses SlugRelatedField.
        
        This test verifies that the content_type field is properly configured
        to use the model name as a string instead of the numeric ID.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        data = serializer.data
        
        # Assert
        self.assertIn('content_type', data)
        # The content_type should be the model name, not the ID
        self.assertEqual(data['content_type'], 'inventory')
    
    def test_serializer_product_info_field(self):
        """
        Test that product_info field is computed correctly.
        
        This test verifies that the product_info field is computed
        and includes information about the related inventory item.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        data = serializer.data
        
        # Assert
        self.assertIn('product_info', data)
        self.assertIsNotNone(data['product_info'])
        # The product_info should contain information about the earwear
        self.assertIsInstance(data['product_info'], dict)
    
    def test_serializer_total_price_field(self):
        """
        Test that total_price field is computed correctly.
        
        This test verifies that the total_price field is computed
        as the product price multiplied by the quantity.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        data = serializer.data
        
        # Assert
        self.assertIn('total_price', data)
        self.assertIsNotNone(data['total_price'])
        # Total price should be price * quantity = 100 * 2 = 200
        expected_total = float(self.inventory.price) * self.shopping_bag.quantity
        self.assertEqual(data['total_price'], expected_total)
    
    def test_serializer_validation_invalid_quantity(self):
        """
        Test serializer validation with invalid quantity.
        
        This test verifies that the serializer properly validates
        the quantity field and rejects invalid values.
        """
        # Arrange
        invalid_data = {
            'content_type': 'inventory',  # Use model name as string
            'object_id': self.inventory.id,  # Use valid inventory ID
            'quantity': -1  # Invalid: must be positive (0 is allowed by PositiveIntegerField)
        }
        
        # Act
        serializer = ShoppingBagSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        
        # Assert
        self.assertFalse(is_valid)
        self.assertIn('quantity', serializer.errors)
    
    def test_serializer_with_guest_user(self):
        """
        Test serializer with guest user data.
        
        This test verifies that the serializer works correctly
        with guest user data instead of authenticated users.
        """
        # Arrange: Create a new guest user and shopping bag
        guest_id = TestDataBuilder.create_guest_id()
        guest_shopping_bag = ShoppingBag.objects.create(
            guest_id=guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=3
        )
        
        # Act
        serializer = ShoppingBagSerializer(guest_shopping_bag)
        data = serializer.data
        
        # Assert
        self.assertIn('id', data)
        self.assertIn('quantity', data)
        self.assertEqual(data['quantity'], 3)
        self.assertIn('total_price', data)
        expected_total = float(self.inventory.price) * 3
        self.assertEqual(data['total_price'], expected_total)
    
    def test_get_product_info_method(self):
        """
        Test the get_product_info method of the serializer.
        
        This test verifies that the get_product_info method
        returns the correct product information.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        product_info = serializer.get_product_info(self.shopping_bag)
        
        # Assert
        self.assertIsInstance(product_info, dict)
        # Check for actual fields that exist in the product_info
        self.assertIn('product_id', product_info)
        self.assertIn('price', product_info)
        self.assertIn('size', product_info)
        self.assertIn('collection', product_info)
        self.assertIn('category', product_info)
    
    def test_get_total_price_method(self):
        """
        Test the get_total_price method of the serializer.
        
        This test verifies that the get_total_price method
        calculates the total price correctly.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)
        
        # Act
        total_price = serializer.get_total_price(self.shopping_bag)
        
        # Assert
        expected_total = float(self.inventory.price) * self.shopping_bag.quantity
        self.assertEqual(total_price, expected_total) 