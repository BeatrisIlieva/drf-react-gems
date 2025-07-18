from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework import status

from src.orders.models import Order
from src.orders.choices import OrderStatusChoices
from src.orders.constants import OrderStatusMessages
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from src.shopping_bags.models import ShoppingBag
from rest_framework.test import APIClient

User = get_user_model()


class OrderViewSetTest(TestCase):
    def setUp(self):
        """Set up test-specific data for each test method."""
        self.client = APIClient()
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

    def test_create_from_shopping_bag_success(self):
        # Arrange
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
        response = self.client.post(
            '/api/orders/create-from-bag/', payment_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('order', response.data)
        self.assertIn('total_items', response.data)
        self.assertIn('total_price', response.data)
        self.assertEqual(response.data['message'],
                         OrderStatusMessages.STATUS_CREATED)

        # Shopping bag should be empty
        self.assertFalse(ShoppingBag.objects.filter(user=self.user).exists())

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
        response = self.client.post(
            '/api/orders/create-from-bag/', invalid_payment_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for any validation error (structure may vary)
        self.assertTrue(len(response.data) > 0)
