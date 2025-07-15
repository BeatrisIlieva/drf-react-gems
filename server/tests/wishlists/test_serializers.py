# Wishlist Serializers Tests
# This module contains tests for the WishlistSerializer to ensure it properly
# serializes and deserializes wishlist data with computed fields.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import uuid
from decimal import Decimal

from src.wishlists.models import Wishlist
from src.wishlists.serializers import WishlistSerializer
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistSerializerTestCase(TestCase):
    """
    Test case for WishlistSerializer.

    This test case verifies that the WishlistSerializer properly handles
    serialization and deserialization of wishlist data, including
    computed fields for product information and ratings.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        """
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.user = cls.shared_data['user']
        cls.guest_id = cls.shared_data['guest_id']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earwear_content_type']

        # Create test wishlist item
        cls.wishlist_item = Wishlist.objects.create(
            user=cls.user,
            content_type=cls.content_type,
            object_id=cls.earwear.id
        )

    def test_serializer_fields(self):
        """
        Test that serializer includes all expected fields.

        This test verifies that the serializer includes all the fields
        defined in the Meta class and that they are properly configured.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        data = serializer.data

        # Assert
        expected_fields = [
            'id', 'user', 'guest_id', 'created_at', 'content_type',
            'object_id', 'product_info'
        ]

        for field in expected_fields:
            self.assertIn(field, data)

    def test_serializer_product_info_field(self):
        """
        Test that product_info field is computed correctly.

        This test verifies that the product_info field is computed
        and includes information about the related product.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        data = serializer.data

        # Assert
        self.assertIn('product_info', data)
        self.assertIsNotNone(data['product_info'])
        # The product_info should contain information about the earwear
        self.assertIsInstance(data['product_info'], dict)

    def test_serializer_with_guest_user(self):
        """
        Test serializer with guest user data.

        This test verifies that the serializer works correctly
        with guest user data instead of authenticated users.
        """
        # Arrange: Create a new guest user and wishlist item
        guest_id = TestDataBuilder.create_guest_id()
        guest_wishlist_item = Wishlist.objects.create(
            guest_id=guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        # Act
        serializer = WishlistSerializer(guest_wishlist_item)
        data = serializer.data

        # Assert
        self.assertIn('id', data)
        self.assertIn('guest_id', data)
        self.assertEqual(str(data['guest_id']), str(guest_id))
        self.assertIn('product_info', data)
        self.assertIsInstance(data['product_info'], dict)

    def test_get_product_info_method(self):
        """
        Test the get_product_info method of the serializer.

        This test verifies that the get_product_info method
        returns the correct product information.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        product_info = serializer.get_product_info(self.wishlist_item)

        # Assert
        self.assertIsInstance(product_info, dict)
        # Check for actual fields that exist in the product_info
        self.assertIn('id', product_info)
        self.assertIn('first_image', product_info)
        self.assertIn('collection__name', product_info)
        self.assertIn('color__name', product_info)

    def test_product_info_average_rating(self):
        """
        Test that product_info includes average rating.

        This test verifies that the product_info field includes
        the average rating for the product.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        product_info = serializer.get_product_info(self.wishlist_item)

        # Assert
        self.assertIn('average_rating', product_info)
        # Average rating should be a number (could be None if no reviews)
        self.assertIsInstance(
            product_info['average_rating'], (int, float, type(None)))

    def test_product_info_price_range(self):
        """
        Test that product_info includes price information.

        This test verifies that the product_info field includes
        price information for the product.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        product_info = serializer.get_product_info(self.wishlist_item)

        # Assert
        self.assertIn('min_price', product_info)
        self.assertIn('max_price', product_info)
        # Price should be a Decimal or number
        self.assertIsInstance(
            product_info['min_price'], (int, float, Decimal, type(None)))
        self.assertIsInstance(
            product_info['max_price'], (int, float, Decimal, type(None)))

    def test_product_info_sold_out_status(self):
        """
        Test that product_info includes sold out status.

        This test verifies that the product_info field includes
        the sold out status for the product.
        """
        # Arrange
        serializer = WishlistSerializer(self.wishlist_item)

        # Act
        product_info = serializer.get_product_info(self.wishlist_item)

        # Assert
        self.assertIn('is_sold_out', product_info)
        # Sold out should be a boolean
        self.assertIsInstance(product_info['is_sold_out'], bool)

    def test_serializer_model_class(self):
        """
        Test that serializer is configured with correct model.

        This test verifies that the serializer is configured
        with the correct model class.
        """
        # Arrange
        serializer = WishlistSerializer()

        # Act & Assert
        from src.wishlists.models import Wishlist
        self.assertEqual(serializer.Meta.model, Wishlist)
