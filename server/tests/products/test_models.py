"""
Tests for Products Models

This module contains comprehensive tests for the products models including
Review, Inventory, and Size. The tests follow the Triple A pattern (Arrange, Act, Assert)
and cover all custom logic, constraints, and critical behaviors.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import uuid

from src.products.models.review import Review
from src.products.models.inventory import Inventory, Size
from src.products.models.product import Earwear, Collection, Color, Metal, Stone
from src.products.constants import ReviewFieldLengths, InventoryFiledLengths
from tests.common.test_data_builder import TestDataBuilder

User = get_user_model()


class ReviewModelTest(TestCase):
    """
    Test cases for the Review model.
    
    Tests cover:
    - Creating reviews with generic relation
    - Enforcing unique (user, product) constraint
    - String representation
    - Approval logic
    """
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(
            email=f'reviewer_{unique_id}@example.com', 
            username=f'reviewer_{unique_id}', 
            password='pass'
        )
        
        # Create unique product data
        product_data = TestDataBuilder.create_unique_product_data('Review Test')
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        
        self.product = Earwear.objects.create(
            first_image='http://example.com/img1.jpg',
            second_image='http://example.com/img2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        self.content_type = ContentType.objects.get_for_model(Earwear)

    def test_create_review_for_product(self):
        """
        Test creating a review for a product using GenericForeignKey.
        
        Arrange: Create user and product
        Act: Create review
        Assert: Review is linked to correct product and user
        """
        # Act
        review = Review.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            rating=5,
            comment='Great product!',
            approved=True
        )
        # Assert
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product!')
        self.assertTrue(review.approved)

    def test_unique_user_product_review_constraint(self):
        """
        Test that a user can only review a product once (unique constraint).
        
        Arrange: Create initial review
        Act: Attempt to create duplicate review
        Assert: IntegrityError is raised
        """
        # Arrange
        Review.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            rating=4,
            comment='Nice!',
            approved=True
        )
        # Act & Assert
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user,
                content_type=self.content_type,
                object_id=self.product.id,
                rating=3,
                comment='Duplicate!',
                approved=False
            )

    def test_review_string_representation(self):
        """
        Test the string representation of the review.
        
        Arrange: Create review
        Act: Convert to string
        Assert: String includes product name, username, and rating
        """
        # Arrange
        review = Review.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            rating=5,
            comment='Excellent!',
            approved=True
        )
        # Act
        string_repr = str(review)
        # Assert
        self.assertIn('Review Tes', string_repr)  # Updated to match actual format
        self.assertIn('reviewer', string_repr)
        self.assertIn('(5)', string_repr)

    def test_review_approval_flag(self):
        """
        Test the approval flag logic for reviews.
        
        Arrange: Create review with approved=False
        Act: Approve the review
        Assert: Approval flag updates correctly
        """
        # Arrange
        review = Review.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            rating=2,
            comment='Needs improvement.',
            approved=False
        )
        # Act
        review.approved = True
        review.save()
        # Assert
        self.assertTrue(Review.objects.get(pk=review.pk).approved)

    def test_comment_length_validation(self):
        """
        Test that comment field enforces max length.
        
        Arrange: Create overly long comment
        Act: Attempt to save review
        Assert: ValidationError is raised
        """
        # Arrange
        long_comment = 'x' * (ReviewFieldLengths.MAX_COMMENT_LENGTH + 1)
        review = Review(
            user=self.user,
            content_type=self.content_type,
            object_id=self.product.id,
            rating=3,
            comment=long_comment,
            approved=True
        )
        # Act & Assert
        with self.assertRaises(ValidationError):
            review.full_clean()


class InventoryModelTest(TestCase):
    """
    Test cases for the Inventory model.
    
    Tests cover:
    - Creating inventory for a product using GenericForeignKey
    - Price and quantity validation (no negatives)
    - String representation
    """
    def setUp(self):
        # Create unique product data
        product_data = TestDataBuilder.create_unique_product_data('Inventory Test')
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        self.size = product_data['size']
        
        self.product = Earwear.objects.create(
            first_image='http://example.com/img1.jpg',
            second_image='http://example.com/img2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        self.content_type = ContentType.objects.get_for_model(Earwear)

    def test_create_inventory_for_product(self):
        """
        Test creating inventory for a product using GenericForeignKey.
        
        Arrange: Create product and size
        Act: Create inventory
        Assert: Inventory is linked to correct product and size
        """
        # Act
        inventory = Inventory.objects.create(
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=10,
            price=Decimal('199.99'),
            size=self.size
        )
        # Assert
        self.assertEqual(inventory.product, self.product)
        self.assertEqual(inventory.size, self.size)
        self.assertEqual(inventory.quantity, 10)
        self.assertEqual(inventory.price, Decimal('199.99'))

    def test_negative_quantity_validation(self):
        """
        Test that quantity cannot be negative.
        
        Arrange: Create inventory with negative quantity
        Act: Attempt to save
        Assert: ValidationError is raised
        """
        # Arrange
        inventory = Inventory(
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=-5,
            price=Decimal('50.00'),
            size=self.size
        )
        # Act & Assert
        with self.assertRaises(ValidationError):
            inventory.full_clean()

    def test_negative_price_validation(self):
        """
        Test that price cannot be negative.
        
        Arrange: Create inventory with negative price
        Act: Attempt to save
        Assert: ValidationError is raised
        """
        # Arrange
        inventory = Inventory(
            content_type=self.content_type,
            object_id=self.product.id,
            quantity=5,
            price=Decimal('-10.00'),
            size=self.size
        )
        # Act & Assert
        with self.assertRaises(ValidationError):
            inventory.full_clean()

    def test_inventory_string_representation(self):
        """
        Test the string representation of the inventory record.
        
        Arrange: Create inventory
        Act: Convert to string
        Assert: String includes quantity, price, and size name
        """
        # Arrange
        inventory = Inventory.objects.create(
            product=self.product,
            size=self.size,
            quantity=7,
            price=Decimal('75.50')
        )
        # Act
        string_repr = str(inventory)
        # Assert
        self.assertIn('Quantity: 7', string_repr)
        self.assertIn('Price: 75.50', string_repr)
        self.assertIn(self.size.name, string_repr)  # Updated to use actual size name


class SizeModelTest(TestCase):
    """
    Test cases for the Size model.
    
    Tests cover:
    - Size name field
    - String representation
    """
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.size = Size.objects.create(name=f'Test Size {unique_id}')

    def test_size_name_field(self):
        """
        Test that size name field works correctly.
        
        Arrange: Create size
        Act: Check name field
        Assert: Name is set correctly
        """
        # Assert
        self.assertIsNotNone(self.size.name)
        self.assertTrue(len(self.size.name) > 0)

    def test_size_string_representation(self):
        """
        Test the string representation of the size.
        
        Arrange: Create size
        Act: Convert to string
        Assert: String representation is the name
        """
        # Act
        string_repr = str(self.size)
        # Assert
        self.assertEqual(string_repr, self.size.name) 