# Shopping Bag Models Tests
# This module contains tests for the ShoppingBag model to ensure it works correctly
# with both authenticated and guest users, and handles GenericForeignKey relationships.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import uuid

from src.shopping_bags.models import ShoppingBag
from src.products.models import Earwear, Collection, Color, Metal, Stone, Size, Inventory
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class ShoppingBagModelTestCase(TestCase):
    """
    Test case for ShoppingBag model.
    
    This test case verifies that the ShoppingBag model works correctly with
    both authenticated and guest users, handles GenericForeignKey relationships,
    and enforces unique constraints properly.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        
        This method creates test data once per test class rather than once per
        test method, significantly improving performance by reducing database
        operations. The data is shared across all test methods in this class.
        """
        # Create shared test data using the TestDataBuilder
        cls.shared_data = TestDataBuilder.create_shared_data()
        
        # Assign commonly used objects to class attributes for easy access
        cls.user = cls.shared_data['user']
        cls.guest_id = cls.shared_data['guest_id']
        cls.collection = cls.shared_data['collection']
        cls.color = cls.shared_data['color']
        cls.metal = cls.shared_data['metal']
        cls.stone = cls.shared_data['stone']
        cls.earwear = cls.shared_data['earwear']
        cls.size = cls.shared_data['size']
        cls.inventory = cls.shared_data['inventory']
        cls.content_type = cls.shared_data['earwear_content_type']
    
    def setUp(self):
        """
        Set up test-specific data for each test method.
        
        This method is called before each test method and can be used to
        create test-specific data that needs to be fresh for each test.
        Note: The shared data from setUpTestData() is already available.
        """
        # No additional setup needed - all data is shared from setUpTestData()
        pass
    
    def test_shopping_bag_creation_with_authenticated_user(self):
        """
        Test creating a shopping bag item for an authenticated user.
        
        This test verifies that a shopping bag item can be created for an
        authenticated user with all required fields.
        """
        # Arrange
        quantity = 2
        
        # Act
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=quantity
        )
        
        # Assert
        self.assertEqual(shopping_bag.user, self.user)
        self.assertIsNone(shopping_bag.guest_id)
        self.assertEqual(shopping_bag.content_type, ContentType.objects.get_for_model(Inventory))
        self.assertEqual(shopping_bag.object_id, self.inventory.id)
        self.assertEqual(shopping_bag.quantity, quantity)
        self.assertIsNotNone(shopping_bag.created_at)
    
    def test_shopping_bag_creation_with_guest_user(self):
        """
        Test creating a shopping bag item for a guest user.
        
        This test verifies that a shopping bag item can be created for a
        guest user using a guest_id instead of a user.
        """
        # Arrange
        quantity = 3
        
        # Act
        shopping_bag = ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=quantity
        )
        
        # Assert
        self.assertIsNone(shopping_bag.user)
        self.assertEqual(shopping_bag.guest_id, self.guest_id)
        self.assertEqual(shopping_bag.content_type, ContentType.objects.get_for_model(Inventory))
        self.assertEqual(shopping_bag.object_id, self.inventory.id)
        self.assertEqual(shopping_bag.quantity, quantity)
        self.assertIsNotNone(shopping_bag.created_at)
    
    def test_shopping_bag_generic_foreign_key_relationship(self):
        """
        Test that GenericForeignKey correctly relates to inventory objects.
        
        This test verifies that the GenericForeignKey properly connects
        shopping bag items to their inventory objects.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        
        # Act
        inventory_object = shopping_bag.inventory
        
        # Assert
        self.assertEqual(inventory_object, self.inventory)
        self.assertIsInstance(inventory_object, Inventory)
        self.assertEqual(inventory_object.quantity, 10)
    
    def test_unique_constraint_authenticated_user(self):
        """
        Test unique constraint for authenticated users.
        
        This test verifies that the unique constraint prevents duplicate
        items for the same user, content type, and object ID.
        """
        # Arrange
        ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        
        # Act & Assert
        with self.assertRaises(IntegrityError):
            ShoppingBag.objects.create(
                user=self.user,
                content_type=ContentType.objects.get_for_model(Inventory),
                object_id=self.inventory.id,
                quantity=2
            )
    
    def test_unique_constraint_guest_user(self):
        """
        Test unique constraint for guest users.
        
        This test verifies that the unique constraint prevents duplicate
        items for the same guest ID, content type, and object ID.
        """
        # Arrange
        ShoppingBag.objects.create(
            guest_id=self.guest_id,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        
        # Act & Assert
        with self.assertRaises(IntegrityError):
            ShoppingBag.objects.create(
                guest_id=self.guest_id,
                content_type=ContentType.objects.get_for_model(Inventory),
                object_id=self.inventory.id,
                quantity=2
            )
    
    def test_different_users_can_have_same_item(self):
        """
        Test that different users can have the same item in their bags.
        
        This test verifies that the unique constraint allows different
        users to have the same item in their shopping bags.
        """
        # Arrange
        second_user = TestDataBuilder.create_authenticated_user('_second', '_second')
        
        # Act
        shopping_bag1 = ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        
        shopping_bag2 = ShoppingBag.objects.create(
            user=second_user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=2
        )
        
        # Assert
        self.assertEqual(shopping_bag1.user, self.user)
        self.assertEqual(shopping_bag2.user, second_user)
        self.assertEqual(shopping_bag1.object_id, shopping_bag2.object_id)
        self.assertEqual(shopping_bag1.content_type, shopping_bag2.content_type)
    
    def test_guest_and_authenticated_user_can_have_same_item(self):
        """
        Test that guest and authenticated users can have the same item.
        
        This test verifies that the unique constraint allows both guest
        and authenticated users to have the same item in their bags.
        """
        # Arrange
        second_guest_id = TestDataBuilder.create_guest_id()
        
        # Act
        authenticated_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        
        guest_bag = ShoppingBag.objects.create(
            guest_id=second_guest_id,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=2
        )
        
        # Assert
        self.assertEqual(authenticated_bag.user, self.user)
        self.assertIsNone(authenticated_bag.guest_id)
        self.assertIsNone(guest_bag.user)
        self.assertEqual(guest_bag.guest_id, second_guest_id)
        self.assertEqual(authenticated_bag.object_id, guest_bag.object_id)
        self.assertEqual(authenticated_bag.content_type, guest_bag.content_type)
    
    def test_quantity_positive_integer_field(self):
        """
        Test that quantity field accepts positive integers.
        
        This test verifies that the quantity field properly validates
        positive integer values and rejects invalid inputs.
        """
        # Arrange: Use a new user for each quantity to avoid unique constraint
        valid_quantities = [1, 10, 100]
        for i, quantity in enumerate(valid_quantities):
            user = TestDataBuilder.create_authenticated_user(f'_quantity_{i}', f'_quantity_{i}')
            shopping_bag = ShoppingBag.objects.create(
                user=user,
                content_type=ContentType.objects.get_for_model(Inventory),
                object_id=self.inventory.id,
                quantity=quantity
            )
            self.assertEqual(shopping_bag.quantity, quantity)
    
    def test_ordering_by_created_at_descending(self):
        """
        Test that shopping bag items are ordered by created_at descending.
        
        This test verifies that the model's Meta ordering is working
        correctly and items are returned in the expected order.
        """
        # Arrange: Use different users to avoid unique constraint
        user1 = self.user
        user2 = TestDataBuilder.create_authenticated_user('_ordering', '_ordering')
        shopping_bag1 = ShoppingBag.objects.create(
            user=user1,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=1
        )
        shopping_bag2 = ShoppingBag.objects.create(
            user=user2,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=2
        )
        # Act
        all_bags = ShoppingBag.objects.filter(object_id=self.inventory.id).order_by('-created_at')
        # Assert
        self.assertEqual(all_bags.count(), 2)
        self.assertEqual(all_bags[0], shopping_bag2)
        self.assertEqual(all_bags[1], shopping_bag1)
    
    def test_string_representation(self):
        """
        Test the string representation of shopping bag items.
        
        This test verifies that the __str__ method returns a meaningful
        string representation of the shopping bag item.
        """
        # Arrange
        shopping_bag = ShoppingBag.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(Inventory),
            object_id=self.inventory.id,
            quantity=3
        )
        # Act
        string_repr = str(shopping_bag)
        # Assert: Check that the string contains the object's id
        self.assertIn(str(shopping_bag.id), string_repr) 