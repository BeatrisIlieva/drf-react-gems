"""
Tests for Product Mixins

This module contains comprehensive tests for the product mixins including
NameFieldMixin and FilterMixin. The tests follow the Triple A pattern
(Arrange, Act, Assert) and cover all mixin functionality including
name field behavior and filtering logic.
"""

from django.test import TestCase
from django.db import models
from unittest.mock import Mock

from src.products.mixins import NameFieldMixin, FilterMixin
from src.products.constants import NameFieldLengths


class TestNameFieldModel(NameFieldMixin):
    """
    Test model that inherits from NameFieldMixin.
    
    This model is used to test the NameFieldMixin functionality
    without affecting the actual database schema.
    """
    class Meta:
        app_label = 'test'


class NameFieldMixinTest(TestCase):
    """
    Test cases for the NameFieldMixin class.
    
    Tests cover:
    - Name field creation and constraints
    - String representation
    - Field validation
    """

    def test_name_field_creation(self):
        """
        Test that the name field is created with correct constraints.
        
        Arrange: Create test model instance
        Act: Check field attributes
        Assert: Field has correct max_length and unique constraint
        """
        # Arrange
        model = TestNameFieldModel()
        
        # Act
        name_field = model._meta.get_field('name')
        
        # Assert
        self.assertEqual(name_field.max_length, NameFieldLengths.NAME_MAX_LENGTH)
        self.assertTrue(name_field.unique)

    def test_name_field_max_length(self):
        """
        Test that the name field uses the correct max length constant.
        
        Arrange: Access the name field
        Act: Check max_length value
        Assert: Uses the constant value
        """
        # Arrange
        model = TestNameFieldModel()
        
        # Act
        name_field = model._meta.get_field('name')
        
        # Assert
        self.assertEqual(name_field.max_length, 30)

    def test_string_representation(self):
        """
        Test the string representation of the model.
        
        Arrange: Create model instance with name
        Act: Convert to string
        Assert: Returns the name field
        """
        # Arrange
        model = TestNameFieldModel()
        model.name = "Test Name"
        
        # Act
        string_repr = str(model)
        
        # Assert
        self.assertEqual(string_repr, "Test Name")

    def test_name_field_type(self):
        """
        Test that the name field is a CharField.
        
        Arrange: Access the name field
        Act: Check field type
        Assert: Field is CharField
        """
        # Arrange
        model = TestNameFieldModel()
        
        # Act
        name_field = model._meta.get_field('name')
        
        # Assert
        self.assertIsInstance(name_field, models.CharField)


class FilterMixinTest(TestCase):
    """
    Test cases for the FilterMixin class.
    
    Tests cover:
    - Parameter extraction from request
    - Filter building for attributes
    - Filter building for products
    """

    def setUp(self):
        """
        Set up test data for each test method.
        
        Creates mock request objects with query parameters for testing
        the filtering functionality.
        """
        # Create mock request with query parameters that has getlist method
        self.mock_request = Mock()
        self.mock_request.query_params = Mock()
        self.mock_request.query_params.getlist = Mock(side_effect=lambda key: {
            'colors': ['1', '2'],
            'stones': ['3'],
            'metals': ['4', '5'],
            'collections': ['6']
        }.get(key, []))

    def test_get_params_extraction(self):
        """
        Test that _get_params correctly extracts filter parameters.
        
        Arrange: Mock request with query parameters
        Act: Call _get_params method
        Assert: Returns correct parameter dictionary
        """
        # Arrange
        mixin = FilterMixin()
        mixin.request = self.mock_request
        
        # Act
        result = mixin._get_params()
        
        # Assert
        self.assertEqual(result['colors'], ['1', '2'])
        self.assertEqual(result['stones'], ['3'])
        self.assertEqual(result['metals'], ['4', '5'])
        self.assertEqual(result['collections'], ['6'])

    def test_get_params_empty_request(self):
        """
        Test that _get_params handles empty request parameters.
        
        Arrange: Mock request with no query parameters
        Act: Call _get_params method
        Assert: Returns empty lists for all parameters
        """
        # Arrange
        empty_request = Mock()
        empty_request.query_params = Mock()
        empty_request.query_params.getlist = Mock(return_value=[])
        
        mixin = FilterMixin()
        mixin.request = empty_request
        
        # Act
        result = mixin._get_params()
        
        # Assert
        self.assertEqual(result['colors'], [])
        self.assertEqual(result['stones'], [])
        self.assertEqual(result['metals'], [])
        self.assertEqual(result['collections'], [])

    def test_get_filters_for_attributes_with_all_params(self):
        """
        Test filter building for attributes with all parameters.
        
        Arrange: Mock request with all filter parameters
        Act: Call _get_filters_for_attributes method
        Assert: Returns Q object with all filter conditions
        """
        # Arrange
        mixin = FilterMixin()
        mixin.request = self.mock_request
        
        # Act
        result = mixin._get_filters_for_attributes('earwear')
        
        # Assert
        # Convert Q object to string to check it contains expected filters
        q_string = str(result)
        self.assertIn('earwear__color_id__in', q_string)
        self.assertIn('earwear__stone_id__in', q_string)
        self.assertIn('earwear__metal_id__in', q_string)
        self.assertIn('earwear__collection_id__in', q_string)

    def test_get_filters_for_attributes_with_no_params(self):
        """
        Test filter building for attributes with no parameters.
        
        Arrange: Mock request with no filter parameters
        Act: Call _get_filters_for_attributes method
        Assert: Returns empty Q object
        """
        # Arrange
        empty_request = Mock()
        empty_request.query_params = Mock()
        empty_request.query_params.getlist = Mock(return_value=[])
        
        mixin = FilterMixin()
        mixin.request = empty_request
        
        # Act
        result = mixin._get_filters_for_attributes('earwear')
        
        # Assert
        # Empty Q object should be falsy
        self.assertFalse(result)

    def test_get_filters_for_attributes_with_partial_params(self):
        """
        Test filter building for attributes with partial parameters.
        
        Arrange: Mock request with only some filter parameters
        Act: Call _get_filters_for_attributes method
        Assert: Returns Q object with only specified filters
        """
        # Arrange
        partial_request = Mock()
        partial_request.query_params = Mock()
        partial_request.query_params.getlist = Mock(side_effect=lambda key: {
            'colors': ['1'],
            'metals': ['2']
        }.get(key, []))
        
        mixin = FilterMixin()
        mixin.request = partial_request
        
        # Act
        result = mixin._get_filters_for_attributes('neckwear')
        
        # Assert
        q_string = str(result)
        self.assertIn('neckwear__color_id__in', q_string)
        self.assertIn('neckwear__metal_id__in', q_string)
        self.assertNotIn('neckwear__stone_id__in', q_string)
        self.assertNotIn('neckwear__collection_id__in', q_string)

    def test_get_filters_for_product_with_all_params(self):
        """
        Test filter building for products with all parameters.
        
        Arrange: Mock request with all filter parameters
        Act: Call _get_filters_for_product method
        Assert: Returns Q object with all filter conditions
        """
        # Arrange
        mixin = FilterMixin()
        mixin.request = self.mock_request
        
        # Act
        result = mixin._get_filters_for_product()
        
        # Assert
        q_string = str(result)
        self.assertIn('color_id__in', q_string)
        self.assertIn('stone_id__in', q_string)
        self.assertIn('metal__id__in', q_string)
        self.assertIn('collection__id__in', q_string)

    def test_get_filters_for_product_with_no_params(self):
        """
        Test filter building for products with no parameters.
        
        Arrange: Mock request with no filter parameters
        Act: Call _get_filters_for_product method
        Assert: Returns empty Q object
        """
        # Arrange
        empty_request = Mock()
        empty_request.query_params = Mock()
        empty_request.query_params.getlist = Mock(return_value=[])
        
        mixin = FilterMixin()
        mixin.request = empty_request
        
        # Act
        result = mixin._get_filters_for_product()
        
        # Assert
        self.assertFalse(result)

    def test_get_filters_for_product_with_partial_params(self):
        """
        Test filter building for products with partial parameters.
        
        Arrange: Mock request with only some filter parameters
        Act: Call _get_filters_for_product method
        Assert: Returns Q object with only specified filters
        """
        # Arrange
        partial_request = Mock()
        partial_request.query_params = Mock()
        partial_request.query_params.getlist = Mock(side_effect=lambda key: {
            'stones': ['1'],
            'collections': ['2']
        }.get(key, []))
        
        mixin = FilterMixin()
        mixin.request = partial_request
        
        # Act
        result = mixin._get_filters_for_product()
        
        # Assert
        q_string = str(result)
        self.assertIn('stone_id__in', q_string)
        self.assertIn('collection__id__in', q_string)
        self.assertNotIn('color_id__in', q_string)
        self.assertNotIn('metal__id__in', q_string) 