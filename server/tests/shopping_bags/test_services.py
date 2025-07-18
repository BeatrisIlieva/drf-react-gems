from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from src.shopping_bags.services import ShoppingBagService
from src.shopping_bags.models import ShoppingBag
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagServiceTestCase(TestCase):

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
        cls.content_type = cls.shared_data['inventory_content_type']

    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create request factory
        self.factory = RequestFactory()

    def test_get_user_identifier_authenticated_user(self):
        """
        This test verifies that the service correctly identifies
        authenticated users and returns appropriate filter parameters.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/')
        request.user = self.user

        # Act
        user_filters = ShoppingBagService.get_user_identifier(request)

        # Assert
        self.assertIn('user', user_filters)
        self.assertEqual(user_filters['user'], self.user)
        self.assertNotIn('guest_id', user_filters)

    def test_get_user_identifier_guest_user(self):
        """
        This test verifies that the service correctly identifies
        guest users and returns appropriate filter parameters.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/')
        request.user = AnonymousUser()
        request.session = {'guest_id': str(self.guest_id)}
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)

        # Act
        user_filters = ShoppingBagService.get_user_identifier(request)

        # Assert
        self.assertIn('guest_id', user_filters)
        self.assertEqual(user_filters['guest_id'], self.guest_id)
        self.assertNotIn('user', user_filters)

    def test_validate_inventory_quantity_sufficient_stock(self):
        """
        This test verifies that the service accepts valid quantities
        when there is sufficient stock available.
        """
        # Arrange
        inventory_obj = self.inventory
        required_quantity = 5

        # Act & Assert
        # Should not raise any exception
        ShoppingBagService.validate_inventory_quantity(
            inventory_obj, required_quantity)

    def test_update_inventory_quantity_reduce_stock(self):
        """
        This test verifies that the service correctly updates
        inventory quantities when reducing stock.
        """
        # Arrange
        inventory_obj = self.inventory
        original_quantity = inventory_obj.quantity
        reduction_amount = 3

        # Act
        ShoppingBagService.update_inventory_quantity(
            inventory_obj, reduction_amount)

        # Assert
        inventory_obj.refresh_from_db()
        self.assertEqual(inventory_obj.quantity,
                         original_quantity - reduction_amount)

    def test_update_inventory_quantity_restore_stock(self):
        """
        This test verifies that the service correctly updates
        inventory quantities when restoring stock.
        """
        # Arrange
        inventory_obj = self.inventory
        original_quantity = inventory_obj.quantity
        restoration_amount = 2

        # Act
        ShoppingBagService.update_inventory_quantity(
            inventory_obj, -restoration_amount)

        # Assert
        inventory_obj.refresh_from_db()
        self.assertEqual(inventory_obj.quantity,
                         original_quantity + restoration_amount)

    def test_get_or_create_bag_item_new_item(self):
        """
        This test verifies that the service creates a new shopping bag item
        when one doesn't exist for the user and product.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user(
            '_new_item', '_new_item')
        filters = {
            'user': user,
            'inventory': self.inventory
        }
        defaults = {'quantity': 2}

        # Act
        bag_item, created = ShoppingBagService.get_or_create_bag_item(
            filters, defaults)

        # Assert
        self.assertTrue(created)
        self.assertEqual(bag_item.user, user)
        self.assertEqual(bag_item.quantity, 2)
        self.assertEqual(bag_item.inventory, self.inventory)

    def test_get_or_create_bag_item_existing_item(self):
        """
        This test verifies that the service retrieves an existing shopping bag item
        when one already exists for the user and product.
        """
        # Arrange
        user = TestDataBuilder.create_authenticated_user(
            '_existing_item', '_existing_item')
        # Create existing bag item
        existing_item = ShoppingBag.objects.create(
            user=user,
            inventory=self.inventory,
            quantity=1
        )
        filters = {
            'user': user,
            'inventory': self.inventory
        }
        defaults = {'quantity': 3}

        # Act
        bag_item, created = ShoppingBagService.get_or_create_bag_item(
            filters, defaults)

        # Assert
        self.assertFalse(created)
        self.assertEqual(bag_item, existing_item)
        # Should not use defaults for existing item
        self.assertEqual(bag_item.quantity, 1)
