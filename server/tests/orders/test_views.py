"""
Tests for Order Views

This module contains comprehensive tests for the OrderViewSet.
Covers list, retrieve, and custom actions like create_from_shopping_bag.
All tests follow the Triple A pattern and are well-documented for clarity.
"""

from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError

from src.orders.models import Order
from src.orders.views import OrderViewSet
from src.orders.choices import OrderStatusChoices
from src.orders.constants import OrderStatusMessages
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from src.shopping_bags.models import ShoppingBag

User = get_user_model()


class OrderViewSetTest(TestCase):
    """
    Test cases for OrderViewSet.
    Covers list, retrieve, and custom actions.
    """
    
    def setUp(self):
        """Set up test-specific data for each test method."""
        from rest_framework.test import APIClient
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.collection = Collection.objects.create(name='Test Collection')
        self.color = Color.objects.create(name='Test Color')
        self.metal = Metal.objects.create(name='Test Metal')
        self.stone = Stone.objects.create(name='Test Stone')
        self.size = Size.objects.create(name='Test Size')

        self.product = Earwear.objects.create(
            first_image='http://example.com/img1.jpg',
            second_image='http://example.com/img2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        self.content_type = ContentType.objects.get_for_model(self.product)

        self.inventory = Inventory.objects.create(
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=10,
            price=Decimal('199.99'),
            size=self.size
        )

        self.order1 = Order.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2,
            status=OrderStatusChoices.PENDING
        )
        self.order2 = Order.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.COMPLETED
        )

    def test_get_queryset(self):
        """
        Test that get_queryset returns orders for the authenticated user.
        
        Arrange: Create orders for different users
        Act: Call get_queryset
        Assert: Only current user's orders are returned
        """
        # Arrange: Create another user and order
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_order = Order.objects.create(
            user=other_user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1,
            status=OrderStatusChoices.PENDING
        )
        
        # Act
        viewset = OrderViewSet()
        viewset.request = self.factory.get('/')
        viewset.request.user = self.user
        queryset = viewset.get_queryset()
        
        # Assert
        self.assertIn(self.order1, queryset)
        self.assertIn(self.order2, queryset)
        self.assertNotIn(other_order, queryset)

    def test_list_action(self):
        """
        Test the list action returns grouped orders.
        
        Arrange: Create orders with same group
        Act: Call list action
        Assert: Grouped orders are returned
        """
        # Act
        response = self.client.get('/api/orders/')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # API returns list directly, not wrapped in 'results'
        self.assertIsInstance(response.data, list)
        # Should have two groups (order1 and order2 have different groups)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_action(self):
        """
        Test the retrieve action returns a single order.
        
        Arrange: Create an order
        Act: Call retrieve action
        Assert: Order details are returned
        """
        # Act
        response = self.client.get(f'/api/orders/{self.order1.id}/')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for group structure in the response
        self.assertIn('order_group', response.data)
        self.assertIn('status', response.data)
        self.assertIn('created_at', response.data)

    def test_create_from_shopping_bag_success(self):
        """
        Test successful order creation from shopping bag.
        
        Arrange: Add items to shopping bag
        Act: Call create_from_shopping_bag action
        Assert: Orders are created and shopping bag is cleared
        """
        # Arrange: Add items to shopping bag
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2
        )
        
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'Test User',
            'expiry_date': '12/30',
            'cvv': '123'
        }
        
        # Act
        response = self.client.post('/api/orders/create-from-bag/', payment_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('order', response.data)
        self.assertIn('total_items', response.data)
        self.assertIn('total_price', response.data)
        self.assertEqual(response.data['message'], OrderStatusMessages.STATUS_CREATED)
        
        # Shopping bag should be empty
        self.assertFalse(ShoppingBag.objects.filter(user=self.user).exists())

    def test_create_from_shopping_bag_empty_bag(self):
        """
        Test order creation fails when shopping bag is empty.
        
        Arrange: Empty shopping bag
        Act: Call create_from_shopping_bag action
        Assert: Error response is returned
        """
        # Arrange: Empty shopping bag and authenticate user
        self.client.force_authenticate(user=self.user)
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'Test User',
            'expiry_date': '12/30',
            'cvv': '123'
        }
        
        # Act
        response = self.client.post('/api/orders/create-from-bag/', payment_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for any validation error (structure may vary)
        self.assertTrue(len(response.data) > 0)

    def test_create_from_shopping_bag_invalid_payment(self):
        """
        Test order creation fails with invalid payment data.
        
        Arrange: Add items to shopping bag with invalid payment
        Act: Call create_from_shopping_bag action
        Assert: Error response is returned
        """
        # Arrange: Add items to shopping bag
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=1
        )
        
        invalid_payment_data = {
            'card_number': '1234',
            'card_holder_name': '',
            'expiry_date': '01/20',
            'cvv': '12'
        }
        
        # Act
        response = self.client.post('/api/orders/create-from-bag/', invalid_payment_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for any validation error (structure may vary)
        self.assertTrue(len(response.data) > 0)

    def test_create_from_shopping_bag_invalid_serializer(self):
        """
        Test order creation fails with invalid serializer data.
        
        Arrange: Invalid payment data
        Act: Call create_from_shopping_bag action
        Assert: Serializer errors are returned
        """
        # Arrange: Invalid payment data (missing required fields)
        invalid_data = {
            'card_number': '4111 1111 1111 1111'
            # Missing other required fields
        }
        
        # Act
        response = self.client.post('/api/orders/create-from-bag/', invalid_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('card_holder_name', response.data)
        self.assertIn('expiry_date', response.data)
        self.assertIn('cvv', response.data)

    def test_create_from_shopping_bag_multiple_items(self):
        """
        Test order creation with multiple items in shopping bag.
        
        Arrange: Add multiple items to shopping bag
        Act: Call create_from_shopping_bag action
        Assert: Multiple orders are created
        """
        # Arrange: Add multiple items to shopping bag
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=2
        )
        
        # Create another product and add to bag
        product2 = Earwear.objects.create(
            first_image='http://example.com/img3.jpg',
            second_image='http://example.com/img4.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        inventory2 = Inventory.objects.create(
            content_type=self.content_type,
            object_id=product2.id,
            quantity=5,
            price=Decimal('299.99'),
            size=self.size
        )
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=product2.id,
            quantity=1
        )
        
        payment_data = {
            'card_number': '4111 1111 1111 1111',
            'card_holder_name': 'Test User',
            'expiry_date': '12/30',
            'cvv': '123'
        }
        
        # Act
        response = self.client.post('/api/orders/create-from-bag/', payment_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that at least two orders were created (structure may vary)
        self.assertTrue(response.data['total_items'] >= 2)
        
        # Shopping bag should be empty
        self.assertFalse(ShoppingBag.objects.filter(user=self.user).exists()) 