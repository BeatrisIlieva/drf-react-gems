"""
Tests for Comment Validator

This module contains comprehensive tests for the validate_comment_length
validator used in the Review model. The tests ensure that the validator
properly enforces the maximum comment length and provides appropriate
error messages.

Tests follow the Triple A pattern (Arrange, Act, Assert) and cover:
- Valid comment lengths (should pass)
- Invalid comment lengths (should raise ValidationError)
- Edge cases (exactly at max length, empty string)
- Error message content and formatting
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from src.products.constants import ReviewFieldLengths
from src.products.validators.comment import validate_comment_length


class ValidateCommentLengthTest(TestCase):
    """
    Test cases for the validate_comment_length validator.
    
    This test class verifies that the validator correctly enforces
    the maximum comment length and provides appropriate error messages
    for invalid input.
    """
    
    def test_valid_comment_length(self):
        """
        Test that comments within the valid length range pass validation.
        
        Arrange: Create a comment string that is within the allowed length
        Act: Call validate_comment_length with the valid comment
        Assert: No ValidationError is raised
        """
        # Arrange: Create a valid comment (within max length)
        valid_comment = "This is a valid comment that should pass validation."
        
        # Act & Assert: Should not raise any exception
        # The validator should accept comments within the limit
        try:
            validate_comment_length(valid_comment)
        except ValidationError:
            self.fail("ValidationError raised for valid comment length")
    
    def test_comment_at_max_length(self):
        """
        Test that comments exactly at the maximum length pass validation.
        
        Arrange: Create a comment string that is exactly at the maximum length
        Act: Call validate_comment_length with the comment at max length
        Assert: No ValidationError is raised
        """
        # Arrange: Create a comment exactly at max length
        max_length_comment = "A" * ReviewFieldLengths.MAX_COMMENT_LENGTH
        
        # Act & Assert: Should not raise any exception
        # Comments exactly at the limit should be accepted
        try:
            validate_comment_length(max_length_comment)
        except ValidationError:
            self.fail("ValidationError raised for comment at max length")
    
    def test_comment_exceeds_max_length(self):
        """
        Test that comments exceeding the maximum length raise ValidationError.
        
        Arrange: Create a comment string that exceeds the maximum length
        Act: Call validate_comment_length with the invalid comment
        Assert: ValidationError is raised with appropriate message
        """
        # Arrange: Create a comment that exceeds max length
        invalid_comment = "A" * (ReviewFieldLengths.MAX_COMMENT_LENGTH + 1)
        
        # Act & Assert: Should raise ValidationError
        with self.assertRaises(ValidationError) as context:
            validate_comment_length(invalid_comment)
        
        # Verify the error message contains the expected information
        error_message = str(context.exception)
        self.assertIn(str(ReviewFieldLengths.MAX_COMMENT_LENGTH), error_message)
        self.assertIn(str(len(invalid_comment)), error_message)
    
    def test_empty_comment(self):
        """
        Test that empty comments pass validation (length validation only).
        
        Note: This test only checks length validation. The blank=False
        constraint in the model would handle empty string validation separately.
        
        Arrange: Create an empty comment string
        Act: Call validate_comment_length with the empty comment
        Assert: No ValidationError is raised
        """
        # Arrange: Create an empty comment
        empty_comment = ""
        
        # Act & Assert: Should not raise any exception
        # Empty strings are within the length limit
        try:
            validate_comment_length(empty_comment)
        except ValidationError:
            self.fail("ValidationError raised for empty comment")
    
    def test_comment_significantly_exceeds_max_length(self):
        """
        Test that comments significantly exceeding the limit raise ValidationError.
        
        Arrange: Create a comment string that is much longer than the limit
        Act: Call validate_comment_length with the very long comment
        Assert: ValidationError is raised with correct length information
        """
        # Arrange: Create a comment much longer than max length
        very_long_comment = "A" * (ReviewFieldLengths.MAX_COMMENT_LENGTH + 100)
        
        # Act & Assert: Should raise ValidationError
        with self.assertRaises(ValidationError) as context:
            validate_comment_length(very_long_comment)
        
        # Verify the error message contains the correct information
        error_message = str(context.exception)
        self.assertIn(str(ReviewFieldLengths.MAX_COMMENT_LENGTH), error_message)
        self.assertIn(str(len(very_long_comment)), error_message)
    
    def test_comment_with_special_characters(self):
        """
        Test that comments with special characters are validated correctly.
        
        Arrange: Create a comment with special characters within the limit
        Act: Call validate_comment_length with the special character comment
        Assert: No ValidationError is raised
        """
        # Arrange: Create a comment with special characters
        special_comment = "Comment with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        # Act & Assert: Should not raise any exception
        # Special characters should be handled the same as regular characters
        try:
            validate_comment_length(special_comment)
        except ValidationError:
            self.fail("ValidationError raised for comment with special characters")
    
    def test_comment_with_unicode_characters(self):
        """
        Test that comments with unicode characters are validated correctly.
        
        Arrange: Create a comment with unicode characters within the limit
        Act: Call validate_comment_length with the unicode comment
        Assert: No ValidationError is raised
        """
        # Arrange: Create a comment with unicode characters
        unicode_comment = "Comment with unicode: éñüßáñöç"
        
        # Act & Assert: Should not raise any exception
        # Unicode characters should be handled correctly
        try:
            validate_comment_length(unicode_comment)
        except ValidationError:
            self.fail("ValidationError raised for comment with unicode characters")
    
    def test_error_message_format(self):
        """
        Test that the error message has the correct format and information.
        
        Arrange: Create a comment that exceeds the limit
        Act: Call validate_comment_length and catch the ValidationError
        Assert: Error message contains expected information
        """
        # Arrange: Create a comment that exceeds max length
        invalid_comment = "A" * (ReviewFieldLengths.MAX_COMMENT_LENGTH + 50)
        
        # Act: Call the validator and catch the exception
        with self.assertRaises(ValidationError) as context:
            validate_comment_length(invalid_comment)
        
        # Assert: Verify the error message format
        error_message = str(context.exception)
        
        # Check that the message contains the maximum allowed length
        self.assertIn(str(ReviewFieldLengths.MAX_COMMENT_LENGTH), error_message)
        
        # Check that the message contains the actual length
        self.assertIn(str(len(invalid_comment)), error_message)
        
        # Check that the message indicates the problem
        self.assertIn("cannot exceed", error_message) 