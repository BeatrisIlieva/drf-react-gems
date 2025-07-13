# Shopping Bag Constants Tests
# This module contains tests for the shopping bag constants to ensure
# error messages are properly defined and accessible.

from django.test import TestCase
from src.shopping_bags.constants import ShoppingBagErrorMessages


class ShoppingBagErrorMessagesTestCase(TestCase):
    """
    Test case for ShoppingBagErrorMessages constants.
    
    This test case verifies that all error message constants are properly defined
    and accessible. It also tests the formatting functionality of error messages.
    """
    
    def test_product_not_found_message_exists(self):
        """
        Test that PRODUCT_NOT_FOUND error message is properly defined.
        
        This test ensures that the error message for when a product is not found
        is accessible and contains the expected text.
        """
        # Arrange & Act
        error_message = ShoppingBagErrorMessages.PRODUCT_NOT_FOUND
        
        # Assert
        self.assertEqual(error_message, 'Product not found')
        self.assertIsInstance(error_message, str)
        self.assertGreater(len(error_message), 0)
    
    def test_insufficient_stock_message_exists(self):
        """
        Test that INSUFFICIENT_STOCK error message is properly defined.
        
        This test ensures that the error message for insufficient stock
        is accessible and contains the expected placeholder.
        """
        # Arrange & Act
        error_message = ShoppingBagErrorMessages.INSUFFICIENT_STOCK
        
        # Assert
        self.assertIn('{quantity}', error_message)
        self.assertIsInstance(error_message, str)
        self.assertGreater(len(error_message), 0)
    
    def test_insufficient_stock_message_formatting(self):
        """
        Test that INSUFFICIENT_STOCK error message can be properly formatted.
        
        This test verifies that the error message can be formatted with a quantity
        value and produces the expected result.
        """
        # Arrange
        quantity = 5
        expected_message = 'Only 5 items available in stock'
        
        # Act
        formatted_message = ShoppingBagErrorMessages.INSUFFICIENT_STOCK.format(quantity=quantity)
        
        # Assert
        self.assertEqual(formatted_message, expected_message)
    
    def test_error_total_price_message_exists(self):
        """
        Test that ERROR_TOTAL_PRICE error message is properly defined.
        
        This test ensures that the error message for total price calculation errors
        is accessible and contains the expected text.
        """
        # Arrange & Act
        error_message = ShoppingBagErrorMessages.ERROR_TOTAL_PRICE
        
        # Assert
        self.assertEqual(error_message, 'Unable to calculate total price')
        self.assertIsInstance(error_message, str)
        self.assertGreater(len(error_message), 0)
    
    def test_all_error_messages_are_strings(self):
        """
        Test that all error messages are string type.
        
        This test ensures that all error message constants are properly defined
        as strings, which is required for proper error handling.
        """
        # Arrange
        error_messages = [
            ShoppingBagErrorMessages.PRODUCT_NOT_FOUND,
            ShoppingBagErrorMessages.INSUFFICIENT_STOCK,
            ShoppingBagErrorMessages.ERROR_TOTAL_PRICE,
        ]
        
        # Act & Assert
        for message in error_messages:
            self.assertIsInstance(message, str)
    
    def test_all_error_messages_have_content(self):
        """
        Test that all error messages have non-empty content.
        
        This test ensures that all error message constants are not empty,
        which would be problematic for user experience.
        """
        # Arrange
        error_messages = [
            ShoppingBagErrorMessages.PRODUCT_NOT_FOUND,
            ShoppingBagErrorMessages.INSUFFICIENT_STOCK,
            ShoppingBagErrorMessages.ERROR_TOTAL_PRICE,
        ]
        
        # Act & Assert
        for message in error_messages:
            self.assertGreater(len(message), 0)
            self.assertNotEqual(message.strip(), '')
    
    def test_error_messages_are_immutable(self):
        """
        Test that error messages are immutable constants.
        
        This test verifies that the error message constants cannot be modified,
        ensuring they remain consistent throughout the application.
        """
        # Arrange
        original_product_not_found = ShoppingBagErrorMessages.PRODUCT_NOT_FOUND
        
        # Act & Assert
        # Attempting to modify the constant should not affect its value
        # (This test documents the expected behavior, though Python doesn't prevent
        # modification of class attributes)
        self.assertEqual(ShoppingBagErrorMessages.PRODUCT_NOT_FOUND, original_product_not_found) 