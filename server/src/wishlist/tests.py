from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework import status
import uuid

from src.wishlist.models import Wishlist
from src.products.models.product import Earwear
from src.products.models.attributes import Collection, Color, Metal, Stone

User = get_user_model()


class WishlistModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        
        # Create test product attributes
        self.collection = Collection.objects.create(name='Test Collection')
        self.color = Color.objects.create(name='Gold')
        self.metal = Metal.objects.create(name='Gold')
        self.stone = Stone.objects.create(name='Diamond')
        
        # Create test product
        self.product = Earwear.objects.create(
            first_image='http://example.com/image1.jpg',
            second_image='http://example.com/image2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        
        self.content_type = ContentType.objects.get_for_model(Earwear)

    def test_create_wishlist_item_for_user(self):
        """Test creating a wishlist item for authenticated user"""
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id
        )
        
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.product, self.product)
        self.assertIsNone(wishlist_item.guest_id)

    def test_create_wishlist_item_for_guest(self):
        """Test creating a wishlist item for guest user"""
        guest_id = uuid.uuid4()
        wishlist_item = Wishlist.objects.create(
            guest_id=guest_id,
            content_type=self.content_type,
            object_id=self.product.id
        )
        
        self.assertEqual(wishlist_item.guest_id, guest_id)
        self.assertEqual(wishlist_item.product, self.product)
        self.assertIsNone(wishlist_item.user)

    def test_wishlist_str_representation(self):
        """Test string representation of wishlist item"""
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id
        )
        
        expected_str = f'{self.user.email} - {self.product}'
        self.assertEqual(str(wishlist_item), expected_str)


class WishlistAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        
        # Create test product attributes
        self.collection = Collection.objects.create(name='Test Collection')
        self.color = Color.objects.create(name='Gold')
        self.metal = Metal.objects.create(name='Gold')
        self.stone = Stone.objects.create(name='Diamond')
        
        # Create test product
        self.product = Earwear.objects.create(
            first_image='http://example.com/image1.jpg',
            second_image='http://example.com/image2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )

    def test_add_product_to_wishlist_authenticated_user(self):
        """Test adding product to wishlist for authenticated user"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'content_type': 'earwear',
            'object_id': self.product.id
        }
        
        response = self.client.post('/wishlist/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if wishlist item was created
        self.assertTrue(
            Wishlist.objects.filter(
                user=self.user,
                object_id=self.product.id
            ).exists()
        )

    def test_add_product_to_wishlist_guest_user(self):
        """Test adding product to wishlist for guest user"""
        guest_id = str(uuid.uuid4())
        
        data = {
            'content_type': 'earwear',
            'object_id': self.product.id,
            'guest_id': guest_id
        }
        
        response = self.client.post('/wishlist/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if wishlist item was created
        self.assertTrue(
            Wishlist.objects.filter(
                guest_id=guest_id,
                object_id=self.product.id
            ).exists()
        )
