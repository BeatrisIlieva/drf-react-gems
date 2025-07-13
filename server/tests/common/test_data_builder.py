"""
Shared Test Data Builder

This module provides a centralized way to create test data that can be shared
across multiple test classes. This significantly reduces database overhead
and improves test performance by avoiding redundant object creation.

The TestDataBuilder uses Django's setUpTestData() pattern to create objects
once per test class rather than once per test method.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import uuid

from src.products.models import Collection, Color, Metal, Stone, Size, Earwear, Inventory

UserModel = get_user_model()


class TestDataBuilder:
    """
    A utility class for creating shared test data across test classes.
    
    This class provides methods to create common test objects (users, products,
    collections, etc.) that can be reused across multiple test classes. This
    significantly improves test performance by reducing database operations.
    
    Usage:
        class MyTestCase(TestCase):
            @classmethod
            def setUpTestData(cls):
                cls.test_data = TestDataBuilder.create_shared_data()
            
            def setUp(self):
                self.user = self.test_data['user']
                self.product = self.test_data['earwear']
                # ... use shared data
    """
    
    @classmethod
    def create_shared_data(cls):
        """
        Create shared test data that can be used across multiple test classes.
        
        This method creates the most commonly used test objects (users, products,
        collections, etc.) once and returns them in a dictionary. This data
        can be shared across all test methods in a class without recreation.
        
        Returns:
            dict: A dictionary containing shared test objects with descriptive keys.
        """
        # Create test user with unique email and username
        user = UserModel.objects.create_user(
            email='shared_test@example.com',
            username='shared_test_user',
            password='SharedTestPass123!'
        )
        
        # Create product-related objects
        collection = Collection.objects.create(name='Shared Test Collection')
        color = Color.objects.create(name='Shared Gold')
        metal = Metal.objects.create(name='Shared Gold')
        stone = Stone.objects.create(name='Shared Diamond')
        size = Size.objects.create(name='Shared Medium')
        
        # Create test earwear product
        earwear = Earwear.objects.create(
            first_image='https://shared.example.com/image1.jpg',
            second_image='https://shared.example.com/image2.jpg',
            collection=collection,
            color=color,
            metal=metal,
            stone=stone
        )
        
        # Create inventory for the earwear
        inventory = Inventory.objects.create(
            quantity=10,
            price=100.00,
            size=size,
            content_type=ContentType.objects.get_for_model(Earwear),
            object_id=earwear.id
        )
        
        # Get content types
        earwear_content_type = ContentType.objects.get_for_model(Earwear)
        inventory_content_type = ContentType.objects.get_for_model(Inventory)
        
        # Create guest ID
        guest_id = uuid.uuid4()
        
        return {
            'user': user,
            'guest_id': guest_id,
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
            'earwear': earwear,
            'inventory': inventory,
            'earwear_content_type': earwear_content_type,
            'inventory_content_type': inventory_content_type,
        }
    
    @classmethod
    def create_authenticated_user(cls, email_suffix='', username_suffix=''):
        """
        Create an authenticated user with unique credentials.
        
        Args:
            email_suffix (str): Optional suffix to make email unique
            username_suffix (str): Optional suffix to make username unique
            
        Returns:
            UserModel: A new authenticated user instance
        """
        unique_id = str(uuid.uuid4())[:8]
        email = f'auth_user{email_suffix}_{unique_id}@example.com'
        username = f'auth_user{username_suffix}_{unique_id}'
        
        return UserModel.objects.create_user(
            email=email,
            username=username,
            password='AuthUserPass123!'
        )
    
    @classmethod
    def create_guest_id(cls):
        """
        Create a new guest ID for testing.
        
        Returns:
            uuid.UUID: A new UUID for guest user testing
        """
        return uuid.uuid4()
    
    @classmethod
    def create_product_with_inventory(cls, product_name='Test Product', price=100.00):
        """
        Create a complete product with inventory for testing.
        
        Args:
            product_name (str): Name for the collection
            price (Decimal): Price for the inventory
            
        Returns:
            dict: Dictionary containing product, inventory, and related objects
        """
        unique_id = str(uuid.uuid4())[:4]  # Shorter ID
        # Create product-related objects
        collection = Collection.objects.create(name=f'{product_name[:10]} Col {unique_id}')
        color = Color.objects.create(name=f'{product_name[:10]} Color {unique_id}')
        metal = Metal.objects.create(name=f'{product_name[:10]} Metal {unique_id}')
        stone = Stone.objects.create(name=f'{product_name[:10]} Stone {unique_id}')
        size = Size.objects.create(name=f'{product_name[:10]} Size {unique_id}')
        
        # Create product
        product = Earwear.objects.create(
            first_image=f'https://{product_name.lower()}.example.com/image1.jpg',
            second_image=f'https://{product_name.lower()}.example.com/image2.jpg',
            collection=collection,
            color=color,
            metal=metal,
            stone=stone
        )
        
        # Create inventory
        inventory = Inventory.objects.create(
            quantity=10,
            price=price,
            size=size,
            content_type=ContentType.objects.get_for_model(Earwear),
            object_id=product.id
        )
        
        return {
            'product': product,
            'inventory': inventory,
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
            'content_type': ContentType.objects.get_for_model(Earwear),
        }
    
    @classmethod
    def create_unique_user(cls, email_prefix='test', username_prefix='testuser'):
        """
        Create a user with guaranteed unique email and username.
        
        Args:
            email_prefix (str): Prefix for email
            username_prefix (str): Prefix for username
            
        Returns:
            UserModel: A new user instance with unique credentials
        """
        unique_id = str(uuid.uuid4())[:8]
        email = f'{email_prefix}_{unique_id}@example.com'
        username = f'{username_prefix}_{unique_id}'
        
        return UserModel.objects.create_user(
            email=email,
            username=username,
            password='TestPass123!'
        )
    
    @classmethod
    def create_unique_product_data(cls, prefix='Test'):
        """
        Create unique product data (collection, color, metal, stone, size).
        
        Args:
            prefix (str): Prefix for product names
            
        Returns:
            dict: Dictionary containing unique product objects
        """
        unique_id = str(uuid.uuid4())[:4]  # Shorter ID
        
        collection = Collection.objects.create(name=f'{prefix[:10]} Col {unique_id}')
        color = Color.objects.create(name=f'{prefix[:10]} Color {unique_id}')
        metal = Metal.objects.create(name=f'{prefix[:10]} Metal {unique_id}')
        stone = Stone.objects.create(name=f'{prefix[:10]} Stone {unique_id}')
        size = Size.objects.create(name=f'{prefix[:10]} Size {unique_id}')
        
        return {
            'collection': collection,
            'color': color,
            'metal': metal,
            'stone': stone,
            'size': size,
        } 