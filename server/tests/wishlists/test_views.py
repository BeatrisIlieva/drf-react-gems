# Wishlist Views Tests
# This module contains tests for the WishlistViewSet to ensure all CRUD operations
# and custom actions work correctly, including proper user identification.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
import uuid

from src.wishlists.models import Wishlist
from src.wishlists.views import WishlistViewSet
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistViewSetTestCase(TestCase):
    """
    Test case for WishlistViewSet.

    This test case verifies that all CRUD operations and custom actions
    work correctly, including proper user identification and wishlist management.
    """

    def setUp(self):
        """
        Set up test data for wishlist view tests.

        This method creates the necessary test data including users, products,
        and API client for testing the ViewSet.
        """
        # Create test user
        self.user = TestDataBuilder.create_unique_user(
            'wishlist', 'wishlist_user')

        # Create test guest ID
        self.guest_id = uuid.uuid4()

        # Create test product data using unique builder
        product_data = TestDataBuilder.create_unique_product_data(
            'Wishlist Test')
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        self.size = product_data['size']

        # Create test earwear product
        self.earwear = Earwear.objects.create(
            first_image='https://example.com/image1.jpg',
            second_image='https://example.com/image2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )

        # Create inventory for the earwear
        self.inventory = Inventory.objects.create(
            quantity=10,
            price=100.00,
            size=self.size,
            content_type=ContentType.objects.get_for_model(Earwear),
            object_id=self.earwear.id
        )

        # Get content type for earwear
        self.content_type = ContentType.objects.get_for_model(Earwear)

        # Create API client
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_get_queryset_authenticated_user(self):
        """
        Test get_queryset for authenticated user.

        This test verifies that the ViewSet correctly filters
        wishlist items for authenticated users.
        """
        # Arrange
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        request = self.factory.get('/api/wishlists/')
        request.user = self.user

        viewset = WishlistViewSet()
        viewset.request = request

        # Act
        queryset = viewset.get_queryset()

        # Assert
        self.assertIn(wishlist_item, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_queryset_guest_user(self):
        """
        Test get_queryset for guest user.

        This test verifies that the ViewSet correctly filters
        wishlist items for guest users.
        """
        # Arrange
        wishlist_item = Wishlist.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.earwear.id
        )

        request = self.factory.get('/api/wishlists/')
        request.user = AnonymousUser()
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)

        viewset = WishlistViewSet()
        viewset.request = request

        # Act
        queryset = viewset.get_queryset()

        # Assert
        self.assertIn(wishlist_item, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_queryset_no_user_identification(self):
        """
        Test get_queryset when user identification fails.

        This test verifies that the ViewSet returns an empty queryset
        when user identification fails.
        """
        # Arrange
        request = self.factory.get('/api/wishlists/')
        request.user = AnonymousUser()
        # No Guest-Id header

        viewset = WishlistViewSet()
        viewset.request = request

        # Act
        queryset = viewset.get_queryset()

        # Assert
        self.assertEqual(queryset.count(), 0)

    def test_viewset_permission_classes(self):
        """
        Test that ViewSet has correct permission classes.

        This test verifies that the ViewSet allows both
        authenticated and guest users to access the API.
        """
        # Arrange
        viewset = WishlistViewSet()

        # Act
        permission_classes = viewset.permission_classes

        # Assert
        from rest_framework.permissions import AllowAny
        self.assertIn(AllowAny, permission_classes)
