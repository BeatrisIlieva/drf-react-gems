from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from src.orders.models import Order
from src.orders.services import PaymentValidationService, OrderService
from src.shopping_bags.models import ShoppingBag
from tests.common.test_data_builder import TestDataBuilder

User = get_user_model()


class PaymentValidationServiceTest(TestCase):

    def test_validate_card_number_valid(self):
        """
        Test that valid card numbers pass validation.
        """
        # VISA
        self.assertTrue(
            PaymentValidationService.validate_card_number(
                '4111 1111 1111 1111'
            )
        )
        # MasterCard Legacy
        self.assertTrue(
            PaymentValidationService.validate_card_number(
                '5100 0000 0000 0000'
            )
        )
        # MasterCard New
        self.assertTrue(
            PaymentValidationService.validate_card_number(
                '2221 0000 0000 0000'
            )
        )

    def test_validate_card_number_invalid(self):
        """
        Test that invalid card numbers raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_number(
                '1234 5678 9012 3456'
            )
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_number('')

    def test_validate_card_holder_name_valid(self):
        """
        Test that valid card holder names pass validation.
        """
        self.assertTrue(
            PaymentValidationService.validate_card_holder_name('John Doe')
        )
        self.assertTrue(
            PaymentValidationService.validate_card_holder_name("O'Connor")
        )
        self.assertTrue(
            PaymentValidationService.validate_card_holder_name(
                'Émilie du Châtelet'
            )
        )

    def test_validate_card_holder_name_invalid(self):
        """
        Test that invalid card holder names raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_holder_name('')
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_holder_name(
                'A'
            )  # Too short
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_holder_name('John123')

    def test_validate_cvv_valid(self):
        """
        Test that valid CVV codes pass validation.
        """
        self.assertTrue(PaymentValidationService.validate_cvv('123'))

    def test_validate_cvv_invalid(self):
        """
        Test that invalid CVV codes raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_cvv('12')
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_cvv('abc')
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_cvv('')

    @patch('src.orders.services.datetime')
    def test_validate_expiry_date_valid(self, mock_datetime):
        """
        Test that valid expiry dates pass validation.
        """
        # Arrange: Set current date to May 2024
        mock_datetime.now.return_value.year = 2024
        mock_datetime.now.return_value.month = 5
        mock_datetime.now.return_value = mock_datetime.now.return_value
        # Act & Assert
        self.assertTrue(PaymentValidationService.validate_expiry_date('06/24'))
        self.assertTrue(PaymentValidationService.validate_expiry_date('12/24'))

    @patch('src.orders.services.datetime')
    def test_validate_expiry_date_invalid(self, mock_datetime):
        """
        Test that invalid or expired expiry dates raise ValidationError.
        """
        # Arrange: Set current date to May 2024
        mock_datetime.now.return_value.year = 2024
        mock_datetime.now.return_value.month = 5
        mock_datetime.now.return_value = mock_datetime.now.return_value
        # Invalid format
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_expiry_date('2024-05')
        # Expired card
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_expiry_date('04/24')
        # Empty
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_expiry_date('')


class OrderServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.user = cls.shared_data['user']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']

    def test_process_order_from_shopping_bag(self):
        user = TestDataBuilder.create_authenticated_user(
            '_order_user', '_order_user'
        )
        ShoppingBag.objects.create(
            user=user, inventory=self.inventory, quantity=2
        )
        orders = OrderService.process_order_from_shopping_bag(user)
        self.assertEqual(len(orders), 1)
        order = orders[0]
        self.assertEqual(order.user, user)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.inventory, self.inventory)
        self.assertFalse(ShoppingBag.objects.filter(user=user).exists())

    def test_process_order_from_empty_shopping_bag(self):
        """
        Test that process_order_from_shopping_bag handles empty shopping bag.
        """
        # Arrange: User with no shopping bag items
        user = TestDataBuilder.create_authenticated_user(
            '_empty_bag', '_empty_bag'
        )

        # Act & Assert
        with self.assertRaises(ValidationError):
            OrderService.process_order_from_shopping_bag(user)

    def test_get_user_orders_and_grouped(self):
        user = TestDataBuilder.create_authenticated_user(
            '_grouped_user', '_grouped_user'
        )
        order1 = Order.objects.create(
            user=user, inventory=self.inventory, quantity=1, status='PE'
        )
        order2 = Order.objects.create(
            user=user, inventory=self.inventory, quantity=2, status='CO'
        )
        orders = OrderService.get_user_orders(user)
        grouped = OrderService.get_user_orders_grouped(user)
        self.assertEqual(orders.count(), 2)
        self.assertIn(str(order1.order_group), grouped)
        self.assertIn(str(order2.order_group), grouped)
