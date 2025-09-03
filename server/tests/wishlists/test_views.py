from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient

from src.wishlists.models import Wishlist
from src.wishlists.views import WishlistViewSet
from src.products.models import DropEarring, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class WishlistViewSetTestCase(TestCase):

    def setUp(self):
        # Create test user
        self.user = TestDataBuilder.create_unique_user(
            'wishlist', 'wishlist_user'
        )

        # Create test product data using unique builder
        product_data = TestDataBuilder.create_unique_product_data(
            'Wishlist Test'
        )
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        self.size = product_data['size']

        # Create test drop_earring product
        self.drop_earring = DropEarring.objects.create(
            first_image='https://example.com/image1.jpg',
            second_image='https://example.com/image2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone,
        )

        # Create inventory for the drop_earring
        self.inventory = Inventory.objects.create(
            quantity=10,
            price=100.00,
            size=self.size,
            content_type=ContentType.objects.get_for_model(DropEarring),
            object_id=self.drop_earring.id,
        )

        # Get content type for drop_earring
        self.content_type = ContentType.objects.get_for_model(DropEarring)

        # Create API client
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_get_queryset_authenticated_user(self):
        """
        This test verifies that the ViewSet correctly filters
        wishlist items for authenticated users.
        """
        # Arrange
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.drop_earring.id,
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
