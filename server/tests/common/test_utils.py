"""
Tests for Common Utils

This module contains comprehensive tests for the common utilities including
ChoicesMaxLengthMixin. The tests follow the Triple A pattern (Arrange, Act, Assert)
and cover all utility functionality including choice field length calculations.
"""

from django.test import TestCase
from django.db import models

from src.common.utils import ChoicesMaxLengthMixin


class TestChoices(ChoicesMaxLengthMixin, models.TextChoices):
    """
    Test choice class for testing ChoicesMaxLengthMixin.
    
    This class inherits from both ChoicesMaxLengthMixin and models.TextChoices
    to test the mixin functionality with Django choice fields.
    """
    SHORT = 'short', 'Short Option'
    MEDIUM = 'medium_length', 'Medium Length Option'
    LONG = 'very_long_option_name', 'Very Long Option Name'


class ChoicesMaxLengthMixinTest(TestCase):
    """
    Test cases for the ChoicesMaxLengthMixin class.
    
    Tests cover:
    - Maximum length calculation for choice values
    - Different choice value lengths
    - Edge cases with empty choices
    """

    def test_max_length_calculation(self):
        """
        Test that max_length correctly calculates the longest choice value.
        
        Arrange: TestChoices class with different length values
        Act: Call max_length method
        Assert: Returns length of longest choice value
        """
        # Arrange: TestChoices class is already defined
        # Act
        result = TestChoices.max_length()
        
        # Assert
        # 'very_long_option_name' is 21 characters long
        self.assertEqual(result, 21)

    def test_max_length_with_single_choice(self):
        """
        Test max_length calculation with only one choice.
        
        Arrange: Custom choice class with single choice
        Act: Call max_length method
        Assert: Returns length of the single choice
        """
        # Arrange
        class SingleChoice(ChoicesMaxLengthMixin, models.TextChoices):
            ONLY = 'single_choice', 'Single Choice'
        
        # Act
        result = SingleChoice.max_length()
        
        # Assert
        self.assertEqual(result, 13)  # 'single_choice' is 13 characters

    def test_max_length_with_empty_choices(self):
        """
        Test max_length calculation with no choices.
        
        Arrange: Custom choice class with no choices
        Act: Call max_length method
        Assert: Raises ValueError due to empty choices
        """
        # Arrange
        class EmptyChoices(ChoicesMaxLengthMixin, models.TextChoices):
            pass
        
        # Act & Assert
        with self.assertRaises(ValueError):
            EmptyChoices.max_length()

    def test_max_length_with_short_choices(self):
        """
        Test max_length calculation with very short choice values.
        
        Arrange: Custom choice class with short values
        Act: Call max_length method
        Assert: Returns length of longest short choice
        """
        # Arrange
        class ShortChoices(ChoicesMaxLengthMixin, models.TextChoices):
            A = 'a', 'A'
            B = 'bb', 'BB'
            C = 'ccc', 'CCC'
        
        # Act
        result = ShortChoices.max_length()
        
        # Assert
        self.assertEqual(result, 3)  # 'ccc' is 3 characters

    def test_max_length_with_special_characters(self):
        """
        Test max_length calculation with choice values containing special characters.
        
        Arrange: Custom choice class with special characters
        Act: Call max_length method
        Assert: Returns correct length including special characters
        """
        # Arrange
        class SpecialChoices(ChoicesMaxLengthMixin, models.TextChoices):
            WITH_DASH = 'with-dash', 'With Dash'
            WITH_UNDERSCORE = 'with_underscore', 'With Underscore'
            WITH_DOT = 'with.dot', 'With Dot'
        
        # Act
        result = SpecialChoices.max_length()
        
        # Assert
        self.assertEqual(result, 15)  # 'with_underscore' is 15 characters

    def test_max_length_with_numbers(self):
        """
        Test max_length calculation with choice values containing numbers.
        
        Arrange: Custom choice class with numeric values
        Act: Call max_length method
        Assert: Returns correct length including numbers
        """
        # Arrange
        class NumericChoices(ChoicesMaxLengthMixin, models.TextChoices):
            ONE = '1', 'One'
            TWENTY_FIVE = '25', 'Twenty Five'
            HUNDRED = '100', 'Hundred'
        
        # Act
        result = NumericChoices.max_length()
        
        # Assert
        self.assertEqual(result, 3)  # '100' is 3 characters

    def test_max_length_consistency(self):
        """
        Test that max_length returns consistent results for the same choices.
        
        Arrange: TestChoices class
        Act: Call max_length multiple times
        Assert: Returns same result each time
        """
        # Arrange: TestChoices class is already defined
        
        # Act
        result1 = TestChoices.max_length()
        result2 = TestChoices.max_length()
        result3 = TestChoices.max_length()
        
        # Assert
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(result1, 21)  # Expected value 