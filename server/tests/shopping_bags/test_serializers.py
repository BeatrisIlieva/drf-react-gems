from django.test import TestCase
from django.contrib.auth import get_user_model


from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.serializers import ShoppingBagSerializer
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagSerializerTestCase(TestCase):

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

        # Create test shopping bag item
        cls.shopping_bag = ShoppingBag.objects.create(
            user=cls.user,
            inventory=cls.inventory,
            quantity=2
        )

    def test_serializer_product_info_field(self):
        """
        This test verifies that the product_info field is computed
        and includes information about the related inventory item.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)

        # Act
        data = serializer.data

        # Assert
        self.assertIn('product_info', data)
        self.assertIsNotNone(data['product_info'])
        # The product_info should contain information about the earwear
        self.assertIsInstance(data['product_info'], dict)

    def test_serializer_total_price_field(self):
        """
        This test verifies that the total_price field is computed
        as the product price multiplied by the quantity.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)

        # Act
        data = serializer.data

        # Assert
        self.assertIn('total_price', data)
        self.assertIsNotNone(data['total_price'])
        # Total price should be price * quantity = 100 * 2 = 200
        expected_total = float(self.inventory.price) * \
            self.shopping_bag.quantity
        self.assertEqual(data['total_price'], expected_total)

    def test_get_product_info_method(self):
        """
        This test verifies that the get_product_info method
        returns the correct product information.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)

        # Act
        product_info = serializer.get_product_info(self.shopping_bag)

        # Assert
        self.assertIsInstance(product_info, dict)
        # Check for actual fields that exist in the product_info
        self.assertIn('product_id', product_info)
        self.assertIn('price', product_info)
        self.assertIn('size', product_info)
        self.assertIn('collection', product_info)
        self.assertIn('category', product_info)

    def test_get_total_price_method(self):
        """
        This test verifies that the get_total_price method
        calculates the total price correctly.
        """
        # Arrange
        serializer = ShoppingBagSerializer(self.shopping_bag)

        # Act
        total_price = serializer.get_total_price(self.shopping_bag)

        # Assert
        expected_total = float(self.inventory.price) * \
            self.shopping_bag.quantity
        self.assertEqual(total_price, expected_total)
