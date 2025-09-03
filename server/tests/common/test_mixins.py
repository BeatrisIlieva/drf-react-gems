from django.test import TestCase
from unittest.mock import Mock

from src.common.mixins import InventoryMixin
from src.products.models.product import DropEarring
from src.products.models.inventory import Inventory


class InventoryMixinTest(TestCase):

    def setUp(self):
        """
        Creates mock objects that simulate inventory and product data
        for testing the mixin functionality.
        """
        # Create mock product with all required attributes
        self.mock_product = Mock(spec=DropEarring)
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
        self.mock_inventory.quantity = 10

        # Create mock object that has inventory and quantity attributes
        self.mock_obj = Mock()
        self.mock_obj.inventory = self.mock_inventory
        self.mock_obj.quantity = 10

        # Set up the relationship between inventory and product
        self.mock_inventory.product = self.mock_product

    def test_get_product_info_success(self):
        # Arrange: Mock objects already set up in setUp()

        # Act
        result = InventoryMixin.get_product_info(self.mock_obj)

        # Assert
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['collection'], "Summer Collection")
        self.assertEqual(result['price'], 150.00)
        self.assertEqual(
            result['first_image'], "https://example.com/image1.jpg"
        )
        self.assertEqual(result['available_quantity'], 10)
        self.assertEqual(result['size'], "Medium")
        self.assertEqual(result['metal'], "Gold")
        self.assertEqual(result['stone'], "Diamond")
        self.assertEqual(result['color'], "Yellow")
        self.assertIn('category', result)
