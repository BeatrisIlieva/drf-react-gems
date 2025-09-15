from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from src.wishlists.models import Wishlist
from src.wishlists.serializers import WishlistSerializer
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistSerializerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        """
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.user = cls.shared_data['user']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earring = cls.shared_data['earring']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earring_content_type']

        # Create test wishlist item
        cls.wishlist_item = Wishlist.objects.create(
            user=cls.user,
            content_type=cls.content_type,
            object_id=cls.earring.id,
        )

    def test_serializer_product_info_field(self):
        """
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
        # The product_info should contain information about the earring
        self.assertIsInstance(data['product_info'], dict)

    def test_get_product_info_method(self):
        """
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
            product_info['average_rating'], (int, float, type(None))
        )

    def test_product_info_price_range(self):
        """
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
            product_info['min_price'], (int, float, Decimal, type(None))
        )
        self.assertIsInstance(
            product_info['max_price'], (int, float, Decimal, type(None))
        )

    def test_product_info_sold_out_status(self):
        """
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
        This test verifies that the serializer is configured
        with the correct model class.
        """
        # Arrange
        serializer = WishlistSerializer()

        # Act & Assert
        from src.wishlists.models import Wishlist

        self.assertEqual(serializer.Meta.model, Wishlist)
