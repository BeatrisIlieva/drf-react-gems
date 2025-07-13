"""
Tests for Order Model

This module contains comprehensive tests for the Order model.
The tests ensure that orders can be created, grouped, and managed correctly.

Tests follow the Triple A pattern (Arrange, Act, Assert) and cover:
- Order creation with different statuses
- Order grouping functionality
- GenericForeignKey relationships
- Status field behavior
- String representation
- Field validation
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from src.orders.models import Order
from src.orders.choices import OrderStatusChoices
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

User = get_user_model()


class OrderModelTest(TestCase):
    """
    Test cases for the Order model.
    
    Tests cover:
    - Order creation with different statuses
    - Order grouping functionality
    - GenericForeignKey relationships
    - Status field behavior
    - String representation
    - Field validation
    """
    
    @classmethod
    def setUpTestData(cls):
        """Set up shared test data for all test methods in this class."""
        cls.shared_data = TestDataBuilder.create_shared_data()
        cls.user = cls.shared_data['user']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.product = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earwear_content_type']
    
    def setUp(self):
        """Set up test-specific data for each test method."""
        pass

    def test_create_order(self):
        """
        Test creating a basic order.
        
        Arrange: Set up user and product data
        Act: Create an order
        Assert: Order is created with correct data
        """
        # Act
        order = Order.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2,
            status=OrderStatusChoices.PENDING
        )
        
        # Assert
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.content_type, self.content_type)
        self.assertEqual(order.object_id, self.product.id)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.status, OrderStatusChoices.PENDING)
        self.assertIsNotNone(order.order_group)
        self.assertIsNotNone(order.created_at)

    def test_order_string_representation(self):
        """
        Test the string representation of an order.
        
        Arrange: Create an order
        Act: Convert order to string
        Assert: String contains expected information
        """
        # Arrange
        order = Order.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        # Act
        string_repr = str(order)
        
        # Assert
        self.assertIn('Order', string_repr)
        self.assertIn(str(order.id), string_repr)
        self.assertIn(self.user.username, string_repr)

    def test_order_status_choices(self):
        """
        Test that order status field accepts valid choices.
        
        Arrange: Create orders with different statuses
        Act: Save orders with different status values
        Assert: Orders are saved with correct statuses
        """
        # Use different users to avoid unique constraint issues
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_status1', '_status1')
        user3 = TestDataBuilder.create_authenticated_user('_status2', '_status2')
        
        # Act & Assert: Test PENDING status
        order_pending = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        self.assertEqual(order_pending.status, OrderStatusChoices.PENDING)
        
        # Act & Assert: Test COMPLETED status
        order_completed = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.COMPLETED
        )
        self.assertEqual(order_completed.status, OrderStatusChoices.COMPLETED)

    def test_order_group_functionality(self):
        """
        Test that orders can be grouped together using order_group.
        
        Arrange: Create multiple orders
        Act: Check order_group values
        Assert: Orders can have same or different group IDs
        """
        # Use different users to avoid unique constraint issues
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_group1', '_group1')
        user3 = TestDataBuilder.create_authenticated_user('_group2', '_group2')
        
        # Act: Create first order
        order1 = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        # Act: Create second order with same group
        order2 = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2,
            status=OrderStatusChoices.PENDING,
            order_group=order1.order_group
        )
        
        # Assert: Both orders have the same group
        self.assertEqual(order1.order_group, order2.order_group)
        
        # Act: Create third order (should get new group)
        order3 = Order.objects.create(
            user=user3,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=3,
            status=OrderStatusChoices.PENDING
        )
        
        # Assert: Third order has different group
        self.assertNotEqual(order1.order_group, order3.order_group)

    def test_generic_foreign_key_relationship(self):
        """
        Test that GenericForeignKey correctly relates to the product.
        
        Arrange: Create an order
        Act: Access the inventory through GenericForeignKey
        Assert: Correct product is returned
        """
        # Arrange
        order = Order.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        # Act
        inventory = order.inventory
        
        # Assert
        self.assertEqual(inventory, self.product)
        self.assertEqual(inventory, self.product)

    def test_quantity_validation(self):
        """
        Test that quantity field accepts positive integers.
        
        Arrange: Create orders with different quantities
        Act: Save orders with various quantity values
        Assert: Orders are saved with correct quantities
        """
        # Use different users to avoid unique constraint issues
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_qty1', '_qty1')
        user3 = TestDataBuilder.create_authenticated_user('_qty2', '_qty2')
        
        # Act & Assert: Test quantity 1
        order1 = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        self.assertEqual(order1.quantity, 1)
        
        # Act & Assert: Test quantity 10
        order2 = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=10,
            status=OrderStatusChoices.PENDING
        )
        self.assertEqual(order2.quantity, 10)
        
        # Act & Assert: Test quantity 100
        order3 = Order.objects.create(
            user=user3,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=100,
            status=OrderStatusChoices.PENDING
        )
        self.assertEqual(order3.quantity, 100)

    def test_order_ordering(self):
        """
        Test that orders are ordered by created_at descending.
        
        Arrange: Create multiple orders
        Act: Query orders with ordering
        Assert: Orders are returned in correct order
        """
        # Use different users to avoid unique constraint issues
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_order1', '_order1')
        user3 = TestDataBuilder.create_authenticated_user('_order2', '_order2')
        
        # Act: Create orders
        order1 = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        order2 = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2,
            status=OrderStatusChoices.PENDING
        )
        
        order3 = Order.objects.create(
            user=user3,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=3,
            status=OrderStatusChoices.PENDING
        )
        
        # Act: Query orders with ordering
        all_orders = Order.objects.filter(object_id=self.product.id).order_by('-created_at')
        
        # Assert: Orders are in correct order (newest first)
        self.assertEqual(all_orders.count(), 3)
        self.assertEqual(all_orders[0], order3)
        self.assertEqual(all_orders[1], order2)
        self.assertEqual(all_orders[2], order1)

    def test_order_with_different_users(self):
        """
        Test that different users can have orders for the same product.
        
        Arrange: Create multiple users
        Act: Create orders for different users
        Assert: Orders are created correctly for each user
        """
        # Arrange: Create additional users
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_diff1', '_diff1')
        user3 = TestDataBuilder.create_authenticated_user('_diff2', '_diff2')
        
        # Act: Create orders for different users
        order1 = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        order2 = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2,
            status=OrderStatusChoices.COMPLETED
        )
        
        order3 = Order.objects.create(
            user=user3,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=3,
            status=OrderStatusChoices.PENDING
        )
        
        # Assert: All orders are created correctly
        self.assertEqual(order1.user, user1)
        self.assertEqual(order2.user, user2)
        self.assertEqual(order3.user, user3)
        self.assertEqual(order1.object_id, order2.object_id)
        self.assertEqual(order2.object_id, order3.object_id)

    def test_order_status_display(self):
        """
        Test that order status display works correctly.
        
        Arrange: Create orders with different statuses
        Act: Check status display values
        Assert: Status display returns correct values
        """
        # Use different users to avoid unique constraint issues
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_display1', '_display1')
        
        # Act: Create orders with different statuses
        order_pending = Order.objects.create(
            user=user1,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        order_completed = Order.objects.create(
            user=user2,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.COMPLETED
        )
        
        # Assert: Status display works correctly
        self.assertEqual(order_pending.get_status_display(), 'Pending')
        self.assertEqual(order_completed.get_status_display(), 'Completed') 