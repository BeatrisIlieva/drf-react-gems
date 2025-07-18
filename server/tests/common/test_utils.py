from django.test import TestCase
from django.db import models

from src.common.utils import ChoicesMaxLengthMixin


class TestChoices(ChoicesMaxLengthMixin, models.TextChoices):
    SHORT = 'short', 'Short Option'
    MEDIUM = 'medium_length', 'Medium Length Option'
    LONG = 'very_long_option_name', 'Very Long Option Name'


class ChoicesMaxLengthMixinTest(TestCase):

    def test_max_length_calculation(self):
        # Arrange: TestChoices class is already defined
        # Act
        result = TestChoices.max_length()

        # Assert
        self.assertEqual(result, 21)
