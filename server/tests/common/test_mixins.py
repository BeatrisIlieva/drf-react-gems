"""
Tests for Common Mixins

This module contains comprehensive tests for the common mixins including
InventoryMixin. The tests follow the Triple A pattern (Arrange, Act, Assert)
and cover all mixin functionality including product information extraction
and price calculations.
"""

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from unittest.mock import Mock, patch

from src.common.mixins import InventoryMixin
from src.products.models.product import Earwear
from src.products.models.inventory import Inventory


class InventoryMixinTest(TestCase):
    """
    Test cases for the InventoryMixin class.
    
    Tests cover:
    - Product information extraction
    - Price calculations
    - Error handling for missing data
    - Dynamic content type handling
    """

    def setUp(self):
        """
        Set up test data for each test method.
        
        Creates mock objects that simulate inventory and product data
        for testing the mixin functionality.
        """
        # Create mock product with all required attributes
        self.mock_product = Mock(spec=Earwear)
        self.mock_product.id = 1
        self.mock_product.collection = "Summer Collection"
        self.mock_product.first_image = "https://example.com/image1.jpg"
        self.mock_product.metal.name = "Gold"
        self.mock_product.stone.name = "Diamond"
        self.mock_product.color.name = "Yellow"

        # Create mock inventory with price
        self.mock_inventory = Mock(spec=Inventory)
        self.mock_inventory.price = 150.00
        self.mock_inventory.size = "Medium"
        self.mock_inventory.quantity = 10  # Explicitly set as int

        # Create mock object that has inventory and quantity attributes
        self.mock_obj = Mock()
        self.mock_obj.inventory = self.mock_inventory
        self.mock_obj.quantity = 10  # Quantity is on the main object

        # Set up the relationship between inventory and product
        self.mock_inventory.product = self.mock_product

    def test_get_product_info_success(self):
        """
        Test successful product information extraction.
        
        Arrange: Mock object with complete inventory and product data
        Act: Call get_product_info method
        Assert: Returns correct product information dictionary
        """
        # Arrange: Mock objects already set up in setUp()
        
        # Act
        result = InventoryMixin.get_product_info(self.mock_obj)
        
        # Assert
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['collection'], "Summer Collection")
        self.assertEqual(result['price'], 150.00)
        self.assertEqual(result['first_image'], "https://example.com/image1.jpg")
        self.assertEqual(result['available_quantity'], 10)
        self.assertEqual(result['size'], "Medium")
        self.assertEqual(result['metal'], "Gold")
        self.assertEqual(result['stone'], "Diamond")
        self.assertEqual(result['color'], "Yellow")
        self.assertIn('category', result)  # Category is dynamically determined

    def test_get_product_info_no_inventory(self):
        """
        Test product info extraction when object has no inventory.
        
        Arrange: Object without inventory attribute
        Act: Call get_product_info method
        Assert: Returns empty dictionary
        """
        # Arrange
        obj_without_inventory = Mock()
        obj_without_inventory.inventory = None
        
        # Act
        result = InventoryMixin.get_product_info(obj_without_inventory)
        
        # Assert
        self.assertEqual(result, {})

    def test_get_product_info_no_product(self):
        """
        Test product info extraction when inventory has no product.
        
        Arrange: Inventory without product attribute
        Act: Call get_product_info method
        Assert: Returns empty dictionary
        """
        # Arrange
        inventory_without_product = Mock()
        inventory_without_product.product = None
        
        obj = Mock()
        obj.inventory = inventory_without_product
        
        # Act
        result = InventoryMixin.get_product_info(obj)
        
        # Assert
        self.assertEqual(result, {})

    def test_get_product_info_missing_size(self):
        """
        Test product info extraction when size attribute is missing.
        
        Arrange: Inventory without size attribute
        Act: Call get_product_info method
        Assert: Returns empty string for size
        """
        # Arrange
        inventory_without_size = Mock()
        inventory_without_size.product = self.mock_product
        inventory_without_size.price = 150.00
        inventory_without_size.quantity = 10
        # Remove size attribute to simulate missing size
        if hasattr(inventory_without_size, 'size'):
            del inventory_without_size.size
        
        obj = Mock()
        obj.inventory = inventory_without_size
        
        # Act
        result = InventoryMixin.get_product_info(obj)
        
        # Assert
        self.assertEqual(result['size'], "")

    @patch('src.common.mixins.ContentType.objects.get_for_model')
    def test_get_product_info_content_type_handling(self, mock_get_for_model):
        """
        Test that ContentType is properly used to determine product category.
        
        Arrange: Mock ContentType and product class
        Act: Call get_product_info method
        Assert: ContentType is called correctly and category is set
        """
        # Arrange
        mock_content_type = Mock()
        mock_content_type.model = "earwear"
        mock_get_for_model.return_value = mock_content_type
        
        # Act
        result = InventoryMixin.get_product_info(self.mock_obj)
        
        # Assert
        mock_get_for_model.assert_called_once_with(self.mock_product.__class__)
        self.assertEqual(result['category'], "Earwear")  # Capitalized

    def test_get_total_price_per_product_success(self):
        """
        Test successful total price calculation.
        
        Arrange: Object with inventory price and quantity
        Act: Call get_total_price_per_product method
        Assert: Returns correct total price
        """
        # Arrange: Mock objects already set up in setUp()
        
        # Act
        result = InventoryMixin.get_total_price_per_product(self.mock_obj)
        
        # Assert
        self.assertEqual(result, 1500.00)  # 150.00 * 10

    def test_get_total_price_per_product_with_decimal(self):
        """
        Test total price calculation with decimal values.
        
        Arrange: Object with decimal price and quantity
        Act: Call get_total_price_per_product method
        Assert: Returns correctly rounded total price
        """
        # Arrange
        inventory_with_decimal = Mock()
        inventory_with_decimal.price = 99.99
        
        obj = Mock()
        obj.inventory = inventory_with_decimal
        obj.quantity = 3
        
        # Act
        result = InventoryMixin.get_total_price_per_product(obj)
        
        # Assert
        self.assertEqual(result, 299.97)  # 99.99 * 3

    def test_get_total_price_per_product_missing_inventory(self):
        """
        Test total price calculation when inventory is missing.
        
        Arrange: Object without inventory attribute
        Act: Call get_total_price_per_product method
        Assert: Returns 0.0 due to exception handling
        """
        # Arrange
        obj_without_inventory = Mock()
        obj_without_inventory.inventory = None
        
        # Act
        result = InventoryMixin.get_total_price_per_product(obj_without_inventory)
        
        # Assert
        self.assertEqual(result, 0.0)

    def test_get_total_price_per_product_missing_quantity(self):
        """
        Test total price calculation when quantity is missing.
        
        Arrange: Object with inventory but no quantity attribute
        Act: Call get_total_price_per_product method
        Assert: Returns 0.0 due to exception handling
        """
        # Arrange
        inventory_without_quantity = Mock()
        inventory_without_quantity.price = 100.00
        
        obj = Mock()
        obj.inventory = inventory_without_quantity
        # No quantity attribute
        
        # Act
        result = InventoryMixin.get_total_price_per_product(obj)
        
        # Assert
        self.assertEqual(result, 0.0)

    def test_get_total_price_per_product_missing_price(self):
        """
        Test total price calculation when price is missing.
        
        Arrange: Object with inventory but no price attribute
        Act: Call get_total_price_per_product method
        Assert: Returns 0.0 due to exception handling
        """
        # Arrange
        inventory_without_price = Mock()
        # No price attribute
        
        obj = Mock()
        obj.inventory = inventory_without_price
        obj.quantity = 5
        
        # Act
        result = InventoryMixin.get_total_price_per_product(obj)
        
        # Assert
        self.assertEqual(result, 0.0) 