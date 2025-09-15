from django.test import TestCase
from unittest.mock import Mock

from src.products.mixins import FilterMixin


class FilterMixinTest(TestCase):

    def setUp(self):
        # Create mock request with query parameters that has getlist method
        self.mock_request = Mock()
        self.mock_request.query_params = Mock()
        self.mock_request.query_params.getlist = Mock(
            side_effect=lambda key: {
                'colors': ['1', '2'],
                'stones': ['3'],
                'metals': ['4', '5'],
                'collections': ['6'],
            }.get(key, [])
        )

    def test_get_params_extraction(self):
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

    def test_get_filters_for_attributes_with_all_params(self):
        # Arrange
        mixin = FilterMixin()
        mixin.request = self.mock_request

        # Act
        result = mixin._get_filters_for_attributes('earring')

        # Assert
        # Convert Q object to string to check it contains expected filters
        q_string = str(result)
        self.assertIn('earring__color_id__in', q_string)
        self.assertIn('earring__stone_id__in', q_string)
        self.assertIn('earring__metal_id__in', q_string)
        self.assertIn('earring__collection_id__in', q_string)

    def test_get_filters_for_product_with_all_params(self):

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
