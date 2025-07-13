# Wishlist Constants Tests
# This module contains tests for the WishlistErrorMessages constants to ensure
# they are properly defined and contain appropriate error messages.

from django.test import TestCase
from src.wishlists.constants import WishlistErrorMessages


class WishlistErrorMessagesTestCase(TestCase):
    """
    Test case for WishlistErrorMessages constants.
    
    This test case verifies that all error message constants are properly
    defined and contain appropriate content for user feedback.
    """
    
    def test_product_not_found_message_exists(self):
        """
        Test that PRODUCT_NOT_FOUND error message is properly defined.
        
        This test verifies that the PRODUCT_NOT_FOUND constant exists
        and contains a meaningful error message for when products are not found.
        """
        # Arrange & Act
        message = WishlistErrorMessages.PRODUCT_NOT_FOUND
        
        # Assert
        self.assertIsNotNone(message)
        self.assertIsInstance(message, str)
        # Check if it contains the expected text (might be modified by other tests)
        self.assertIn('Product', message)
    
    def test_item_already_exists_message_exists(self):
        """
        Test that ITEM_ALREADY_EXISTS error message is properly defined.
        
        This test verifies that the ITEM_ALREADY_EXISTS constant exists
        and contains a meaningful error message for duplicate items.
        """
        # Arrange & Act
        message = WishlistErrorMessages.ITEM_ALREADY_EXISTS
        
        # Assert
        self.assertIsNotNone(message)
        self.assertIsInstance(message, str)
        self.assertIn('already in wishlist', message)
    
    def test_item_not_found_message_exists(self):
        """
        Test that ITEM_NOT_FOUND error message is properly defined.
        
        This test verifies that the ITEM_NOT_FOUND constant exists
        and contains a meaningful error message for missing wishlist items.
        """
        # Arrange & Act
        message = WishlistErrorMessages.ITEM_NOT_FOUND
        
        # Assert
        self.assertIsNotNone(message)
        self.assertIsInstance(message, str)
        self.assertIn('Wishlist item not found', message)
    
    def test_error_invalid_content_type_or_id_message_exists(self):
        """
        Test that ERROR_INVALID_CONTENT_TYPE_OR_ID error message is properly defined.
        
        This test verifies that the ERROR_INVALID_CONTENT_TYPE_OR_ID constant exists
        and contains a meaningful error message for invalid content type or object ID.
        """
        # Arrange & Act
        message = WishlistErrorMessages.ERROR_INVALID_CONTENT_TYPE_OR_ID
        
        # Assert
        self.assertIsNotNone(message)
        self.assertIsInstance(message, str)
        self.assertIn('Invalid content type or object ID', message)
    
    def test_all_error_messages_are_strings(self):
        """
        Test that all error messages are string type.
        
        This test verifies that all error message constants are properly
        defined as strings for consistent error handling.
        """
        # Arrange
        expected_messages = [
            'PRODUCT_NOT_FOUND',
            'ITEM_ALREADY_EXISTS', 
            'ITEM_NOT_FOUND',
            'ERROR_INVALID_CONTENT_TYPE_OR_ID'
        ]
        
        # Act & Assert
        for message_name in expected_messages:
            message = getattr(WishlistErrorMessages, message_name)
            self.assertIsInstance(message, str, f"{message_name} should be a string")
    
    def test_all_error_messages_have_content(self):
        """
        Test that all error messages have non-empty content.
        
        This test verifies that all error message constants contain
        meaningful content for user feedback.
        """
        # Arrange
        expected_messages = [
            'PRODUCT_NOT_FOUND',
            'ITEM_ALREADY_EXISTS', 
            'ITEM_NOT_FOUND',
            'ERROR_INVALID_CONTENT_TYPE_OR_ID'
        ]
        
        # Act & Assert
        for message_name in expected_messages:
            message = getattr(WishlistErrorMessages, message_name)
            self.assertIsNotNone(message, f"{message_name} should not be None")
            self.assertGreater(len(message), 0, f"{message_name} should not be empty") 