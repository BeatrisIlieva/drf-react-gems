"""
Tests for Order Services

This module contains comprehensive tests for the PaymentValidationService and OrderService.
Covers card validation, order processing, grouping, and total calculation.
All tests follow the Triple A pattern and are well-documented for clarity.
"""

from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, NotFound

from src.orders.models import Order
from src.orders.services import PaymentValidationService, OrderService
from src.orders.constants import CardErrorMessages
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from src.shopping_bags.models import ShoppingBag
from tests.common.test_data_builder import TestDataBuilder

User = get_user_model()

class PaymentValidationServiceTest(TestCase):
    """
    Test cases for PaymentValidationService.
    Covers card number, holder name, CVV, and expiry date validation.
    """
    def test_validate_card_number_valid(self):
        """
        Test that valid card numbers pass validation.
        """
        # VISA
        self.assertTrue(PaymentValidationService.validate_card_number('4111 1111 1111 1111'))
        # MasterCard Legacy
        self.assertTrue(PaymentValidationService.validate_card_number('5100 0000 0000 0000'))
        # MasterCard New
        self.assertTrue(PaymentValidationService.validate_card_number('2221 0000 0000 0000'))

    def test_validate_card_number_invalid(self):
        """
        Test that invalid card numbers raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_number('1234 5678 9012 3456')
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_number('')

    def test_validate_card_holder_name_valid(self):
        """
        Test that valid card holder names pass validation.
        """
        self.assertTrue(PaymentValidationService.validate_card_holder_name('John Doe'))
        self.assertTrue(PaymentValidationService.validate_card_holder_name("O'Connor"))
        self.assertTrue(PaymentValidationService.validate_card_holder_name('Émilie du Châtelet'))

    def test_validate_card_holder_name_invalid(self):
        """
        Test that invalid card holder names raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_holder_name('')
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_card_holder_name('A')  # Too short
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

    def test_validate_payment_data_valid(self):
        """
        Test that valid payment data passes validation.
        """
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'John Doe',
            'cvv': '123',
            'expiry_date': '12/30',
        }
        self.assertTrue(PaymentValidationService.validate_payment_data(payment_data))

    def test_validate_payment_data_invalid(self):
        """
        Test that invalid payment data raises ValidationError.
        """
        payment_data = {
            'card_number': '1234',
            'card_holder_name': '',
            'cvv': '12',
            'expiry_date': '01/20',
        }
        with self.assertRaises(ValidationError):
            PaymentValidationService.validate_payment_data(payment_data)

class OrderServiceTest(TestCase):
    """
    Test cases for OrderService.
    Covers order processing, grouping, and total calculation.
    """
    
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
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earwear_content_type']

    def test_get_user_identifier(self):
        """
        Test that get_user_identifier delegates to UserIdentificationService.
        """
        class DummyRequest:
            pass
        with patch('src.common.services.UserIdentificationService.get_user_identifier', return_value={'id': 1}):
            result = OrderService.get_user_identifier(DummyRequest())
            self.assertEqual(result, {'id': 1})

    def test_get_inventory_object_valid(self):
        """
        Test that get_inventory_object returns the correct product.
        """
        obj = OrderService.get_inventory_object(self.content_type, self.earwear.id)
        self.assertEqual(obj, self.earwear)

    def test_get_inventory_object_invalid(self):
        """
        Test that get_inventory_object raises NotFound for invalid object.
        """
        with self.assertRaises(NotFound):
            OrderService.get_inventory_object(self.content_type, 9999)

    def test_process_order_from_shopping_bag(self):
        """
        Test that process_order_from_shopping_bag creates orders correctly.
        """
        # Arrange: Create shopping bag items
        user = TestDataBuilder.create_authenticated_user('_order_user', '_order_user')
        shopping_bag_item = ShoppingBag.objects.create(
            user=user,
            content_type=self.content_type,
            object_id=self.earwear.id,
            quantity=2
        )
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'Test User',
            'cvv': '123',
            'expiry_date': '12/30',
        }
        
        # Act
        orders = OrderService.process_order_from_shopping_bag(user, payment_data)
        
        # Assert
        self.assertEqual(len(orders), 1)
        order = orders[0]
        self.assertEqual(order.user, user)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.object_id, self.earwear.id)
        
        # Verify shopping bag was cleared
        self.assertFalse(ShoppingBag.objects.filter(user=user).exists())

    def test_process_order_from_empty_shopping_bag(self):
        """
        Test that process_order_from_shopping_bag handles empty shopping bag.
        """
        # Arrange: User with no shopping bag items
        user = TestDataBuilder.create_authenticated_user('_empty_bag', '_empty_bag')
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'Test User',
            'cvv': '123',
            'expiry_date': '12/30',
        }
        
        # Act & Assert
        with self.assertRaises(ValidationError):
            OrderService.process_order_from_shopping_bag(user, payment_data)

    def test_get_user_orders_and_grouped(self):
        """
        Test that get_user_orders_and_grouped returns correct data structure.
        """
        # Arrange: Create some orders for the user
        user = TestDataBuilder.create_authenticated_user('_grouped_user', '_grouped_user')
        order1 = Order.objects.create(
            user=user,
            content_type=self.content_type,
            object_id=self.earwear.id,
            quantity=1,
            status='PE'
        )
        order2 = Order.objects.create(
            user=user,
            content_type=self.content_type,
            object_id=self.earwear.id,
            quantity=2,
            status='CO'
        )
        
        # Act
        orders = OrderService.get_user_orders(user)
        grouped = OrderService.get_user_orders_grouped(user)
        
        # Assert
        self.assertEqual(orders.count(), 2)
        self.assertIn(str(order1.order_group), grouped)
        self.assertIn(str(order2.order_group), grouped) 