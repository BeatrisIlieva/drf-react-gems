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
