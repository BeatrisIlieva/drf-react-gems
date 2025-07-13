# Shopping Bag Views Tests
# This module contains tests for the ShoppingBagViewSet to ensure all CRUD operations
# and custom actions work correctly, including proper user identification and inventory management.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import uuid
from django.contrib.auth.models import AnonymousUser

from src.shopping_bags.models import ShoppingBag
from src.shopping_bags.views import ShoppingBagViewSet
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagViewSetTestCase(TestCase):
    """
    Test case for ShoppingBagViewSet.
    
    This test case verifies that all CRUD operations and custom actions
    work correctly, including proper user identification and inventory management.
    """
    
    def setUp(self):
        """
        Set up test data for shopping bag view tests.
        
        This method creates the necessary test data including users, products,
        and API client for testing the ViewSet.
        """
        # Create test user
        self.user = TestDataBuilder.create_unique_user('shopping_bag', 'shopping_bag_user')
        
        # Create test guest ID
        self.guest_id = uuid.uuid4()
        
        # Create test product data using unique builder
        product_data = TestDataBuilder.create_unique_product_data('Shopping Bag Test')
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
        
        # Get content type for inventory
        self.content_type = ContentType.objects.get_for_model(Inventory)
        
        # Create API client
        self.client = APIClient()
        self.factory = RequestFactory()
    
    def test_get_queryset_authenticated_user(self):
        """
        Test get_queryset for authenticated user.
        
        This test verifies that the ViewSet correctly filters
        shopping bag items for authenticated users.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        request = self.factory.get('/api/shopping-bags/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        queryset = viewset.get_queryset()
        
        # Assert
        self.assertIn(shopping_bag, queryset)
        self.assertEqual(queryset.count(), 1)
    
    def test_get_queryset_guest_user(self):
        """
        Test get_queryset for guest user.
        
        This test verifies that the ViewSet correctly filters
        shopping bag items for guest users.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        request = self.factory.get('/api/shopping-bags/')
        request.user = AnonymousUser()
        request.session = {'guest_id': str(self.guest_id)}
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        queryset = viewset.get_queryset()
        
        # Assert
        self.assertIn(shopping_bag, queryset)
        self.assertEqual(queryset.count(), 1)
    
    def test_get_queryset_no_user_identification(self):
        """
        Test get_queryset when user identification fails.
        
        This test verifies that the ViewSet returns an empty queryset
        when user identification fails.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/')
        request.user = AnonymousUser()
        request.session = {}  # No guest_id
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        queryset = viewset.get_queryset()
        
        # Assert
        self.assertEqual(queryset.count(), 0)
    
    def test_perform_create_new_item(self):
        """
        Test perform_create for new shopping bag item.
        
        This test verifies that the ViewSet correctly creates
        new shopping bag items with proper inventory validation.
        """
        # Arrange
        request = self.factory.post('/api/shopping-bags/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Mock serializer with validated data
        class MockSerializer:
            def __init__(self, inventory):
                self.validated_data = {
                    'content_type': ContentType.objects.get_for_model(Inventory),
                    'object_id': inventory.id,
                    'quantity': 2
                }
                self.instance = None
        
        serializer = MockSerializer(self.inventory)
        
        # Act
        viewset.perform_create(serializer)
        
        # Assert
        self.assertIsNotNone(serializer.instance)
        self.assertEqual(serializer.instance.user, self.user)
        self.assertEqual(serializer.instance.quantity, 2)
        
        # Check that inventory was updated
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 8)  # 10 - 2
    
    def test_perform_create_existing_item(self):
        """
        Test perform_create for existing shopping bag item.
        
        This test verifies that the ViewSet correctly updates
        existing shopping bag items by adding to quantity.
        """
        # Arrange
        existing_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        request = self.factory.post('/api/shopping-bags/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Mock serializer with validated data
        class MockSerializer:
            def __init__(self, inventory):
                self.validated_data = {
                    'content_type': ContentType.objects.get_for_model(Inventory),
                    'object_id': inventory.id,
                    'quantity': 2
                }
                self.instance = None
        
        serializer = MockSerializer(self.inventory)
        
        # Act
        viewset.perform_create(serializer)
        
        # Assert
        self.assertIsNotNone(serializer.instance)
        self.assertEqual(serializer.instance.id, existing_bag.id)
        self.assertEqual(serializer.instance.quantity, 3)  # 1 + 2
        
        # Check that inventory was updated
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 8)  # 10 - 2
    
    def test_perform_update_increase_quantity(self):
        """
        Test perform_update to increase quantity.
        
        This test verifies that the ViewSet correctly updates
        shopping bag item quantities with proper validation.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        request = self.factory.put('/api/shopping-bags/1/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Mock get_object to return our shopping bag
        def mock_get_object():
            return shopping_bag
        
        viewset.get_object = mock_get_object
        
        # Mock serializer with validated data
        class MockSerializer:
            def __init__(self):
                self.validated_data = {'quantity': 3}
            
            def save(self):
                shopping_bag.quantity = 3
                shopping_bag.save()
        
        serializer = MockSerializer()
        
        # Act
        viewset.perform_update(serializer)
        
        # Assert
        shopping_bag.refresh_from_db()
        self.assertEqual(shopping_bag.quantity, 3)
        
        # Check that inventory was updated (additional 2 items)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 8)  # 10 - 2
    
    def test_perform_update_decrease_quantity(self):
        """
        Test perform_update to decrease quantity.
        
        This test verifies that the ViewSet correctly updates
        shopping bag item quantities when decreasing.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=3
        )
        
        request = self.factory.put('/api/shopping-bags/1/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Mock get_object to return our shopping bag
        def mock_get_object():
            return shopping_bag
        
        viewset.get_object = mock_get_object
        
        # Mock serializer with validated data
        class MockSerializer:
            def __init__(self):
                self.validated_data = {'quantity': 1}
            
            def save(self):
                shopping_bag.quantity = 1
                shopping_bag.save()
        
        serializer = MockSerializer()
        
        # Act
        viewset.perform_update(serializer)
        
        # Assert
        shopping_bag.refresh_from_db()
        self.assertEqual(shopping_bag.quantity, 1)
        
        # Check that inventory was restored (2 items back)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 12)  # 10 + 2
    
    def test_perform_update_zero_quantity_deletes_item(self):
        """
        Test perform_update with zero quantity deletes item.
        
        This test verifies that the ViewSet correctly deletes
        shopping bag items when quantity becomes zero.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        request = self.factory.put('/api/shopping-bags/1/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Mock get_object to return our shopping bag
        def mock_get_object():
            return shopping_bag
        
        viewset.get_object = mock_get_object
        
        # Mock serializer with validated data
        class MockSerializer:
            def __init__(self):
                self.validated_data = {'quantity': 0}
        
        serializer = MockSerializer()
        
        # Mock perform_destroy
        def mock_perform_destroy(instance):
            instance.delete()
        
        viewset.perform_destroy = mock_perform_destroy
        
        # Act
        viewset.perform_update(serializer)
        
        # Assert
        # Item should be deleted
        self.assertFalse(ShoppingBag.objects.filter(id=shopping_bag.id).exists())
        
        # Refresh inventory from db and check quantity
        inventory = Inventory.objects.get(id=shopping_bag.object_id)
        inventory.refresh_from_db()
        self.assertEqual(inventory.quantity, 10)  # Original quantity restored
    
    def test_perform_destroy_restores_inventory(self):
        """
        Test perform_destroy restores inventory quantity.
        
        This test verifies that the ViewSet correctly restores
        inventory quantity when deleting shopping bag items.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=3
        )
        
        request = self.factory.delete('/api/shopping-bags/1/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        viewset.perform_destroy(shopping_bag)
        
        # Assert
        # Item should be deleted
        self.assertFalse(ShoppingBag.objects.filter(id=shopping_bag.id).exists())
        
        # Check that inventory was restored
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 13)  # 10 + 3
    
    def test_get_bag_count_authenticated_user(self):
        """
        Test get_bag_count for authenticated user.
        
        This test verifies that the custom action correctly
        calculates the total count of items in the shopping bag.
        """
        # Arrange
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        request = self.factory.get('/api/shopping-bags/count/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_bag_count(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_get_bag_count_guest_user(self):
        """
        Test get_bag_count for guest user.
        
        This test verifies that the custom action correctly
        calculates the total count for guest users.
        """
        # Arrange
        ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        request = self.factory.get('/api/shopping-bags/count/')
        request.user = AnonymousUser()
        request.session = {'guest_id': str(self.guest_id)}
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_bag_count(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_get_bag_count_empty_bag(self):
        """
        Test get_bag_count for empty shopping bag.
        
        This test verifies that the custom action returns zero
        when the shopping bag is empty.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/count/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_bag_count(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    
    def test_get_total_price_authenticated_user(self):
        """
        Test get_total_price for authenticated user.
        
        This test verifies that the custom action correctly
        calculates the total price of items in the shopping bag.
        """
        # Arrange
        ShoppingBag.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=2
        )
        
        request = self.factory.get('/api/shopping-bags/total-price/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_total_price(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_total = float(self.inventory.price) * 2
        self.assertEqual(response.data['total_price'], expected_total)
    
    def test_get_total_price_guest_user(self):
        """
        Test get_total_price for guest user.
        
        This test verifies that the custom action correctly
        calculates the total price for guest users.
        """
        # Arrange
        ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=self.content_type,
            object_id=self.inventory.id,
            quantity=1
        )
        
        request = self.factory.get('/api/shopping-bags/total-price/')
        request.user = AnonymousUser()
        request.session = {'guest_id': str(self.guest_id)}
        request.META['HTTP_GUEST_ID'] = str(self.guest_id)
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_total_price(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_total = float(self.inventory.price) * 1
        self.assertEqual(response.data['total_price'], expected_total)
    
    def test_get_total_price_empty_bag(self):
        """
        Test get_total_price for empty shopping bag.
        
        This test verifies that the custom action returns zero
        when the shopping bag is empty.
        """
        # Arrange
        request = self.factory.get('/api/shopping-bags/total-price/')
        request.user = self.user
        
        viewset = ShoppingBagViewSet()
        viewset.request = request
        
        # Act
        response = viewset.get_total_price(request)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], 0.0)
    
    def test_viewset_permission_classes(self):
        """
        Test that ViewSet has correct permission classes.
        
        This test verifies that the ViewSet allows both
        authenticated and guest users to access the API.
        """
        # Arrange
        viewset = ShoppingBagViewSet()
        
        # Act
        permission_classes = viewset.permission_classes
        
        # Assert
        from rest_framework.permissions import AllowAny
        self.assertIn(AllowAny, permission_classes)
    
    def test_viewset_serializer_class(self):
        """
        Test that ViewSet has correct serializer class.
        
        This test verifies that the ViewSet uses the correct
        serializer for handling shopping bag data.
        """
        # Arrange
        viewset = ShoppingBagViewSet()
        
        # Act
        serializer_class = viewset.serializer_class
        
        # Assert
        from src.shopping_bags.serializers import ShoppingBagSerializer
        self.assertEqual(serializer_class, ShoppingBagSerializer) 