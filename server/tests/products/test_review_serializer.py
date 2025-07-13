"""
Test module for ReviewSerializer functionality.

This module tests the ReviewSerializer to ensure it properly includes
the approved field and handles review approval status correctly.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework import status

from src.products.models.product import Earwear
from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from src.products.serializers.base import BaseProductItemSerializer
from tests.common.test_data_builder import TestDataBuilder

User = get_user_model()


class ReviewSerializerTest(TestCase):
    """
    Test cases for ReviewSerializer functionality.
    
    This class tests that the ReviewSerializer properly includes
    the approved field and handles review data correctly.
    """
    
    def setUp(self):
        """Set up test data for review serializer tests."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test product data
        product_data = TestDataBuilder.create_unique_product_data('Test Product')
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        
        # Create test product
        self.product = Earwear.objects.create(
            first_image='http://example.com/img1.jpg',
            second_image='http://example.com/img2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        
        # Get content type for the product
        self.content_type = ContentType.objects.get_for_model(Earwear)
        
        # Create test reviews
        self.approved_review = Review.objects.create(
            user=self.user,
            rating=5,
            comment='Great product!',
            content_type=self.content_type,
            object_id=self.product.id,
            approved=True
        )
        
        self.unapproved_review = Review.objects.create(
            user=self.user,
            rating=4,
            comment='Good product',
            content_type=self.content_type,
            object_id=self.product.id,
            approved=False
        )
    
    def test_review_serializer_includes_approved_field(self):
        """
        Test that ReviewSerializer includes the approved field in serialized data.
        
        This ensures that the approval status is properly included
        in the serialized review data for frontend consumption.
        """
        # Serialize an approved review
        serializer = ReviewSerializer(self.approved_review)
        data = serializer.data
        
        # Verify approved field is present and correct
        self.assertIn('approved', data)
        self.assertTrue(data['approved'])
        
        # Serialize an unapproved review
        serializer = ReviewSerializer(self.unapproved_review)
        data = serializer.data
        
        # Verify approved field is present and correct
        self.assertIn('approved', data)
        self.assertFalse(data['approved'])
    
    def test_review_serializer_includes_all_required_fields(self):
        """
        Test that ReviewSerializer includes all required fields.
        
        This ensures that all necessary review data is properly
        serialized for the frontend.
        """
        serializer = ReviewSerializer(self.approved_review)
        data = serializer.data
        
        # Check that all expected fields are present
        expected_fields = [
            'id', 'user', 'rating', 'comment', 'created_at',
            'content_type', 'object_id', 'photo_url', 'user_full_name', 'approved'
        ]
        
        for field in expected_fields:
            self.assertIn(field, data, f"Field '{field}' should be present in serialized data")


class ProductSerializerReviewVisibilityTest(APITestCase):
    """
    Test cases for product serializer review visibility logic.
    
    This class tests that the product serializer correctly shows
    unapproved reviews to reviewers and only approved reviews to regular users.
    """
    
    def setUp(self):
        """Set up test data for product serializer tests."""
        # Create test users
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123'
        )
        
        self.reviewer_user = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='testpass123'
        )
        
        # Add reviewer permission to reviewer user
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        
        review_content_type = ContentType.objects.get_for_model(Review)
        approve_permission = Permission.objects.get(
            content_type=review_content_type,
            codename='approve_review'
        )
        self.reviewer_user.user_permissions.add(approve_permission)
        
        # Create test product data
        product_data = TestDataBuilder.create_unique_product_data('Test Product')
        self.collection = product_data['collection']
        self.color = product_data['color']
        self.metal = product_data['metal']
        self.stone = product_data['stone']
        
        # Create test product
        self.product = Earwear.objects.create(
            first_image='http://example.com/img1.jpg',
            second_image='http://example.com/img2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )
        
        # Get content type for the product
        self.content_type = ContentType.objects.get_for_model(Earwear)
        
        # Create test reviews
        self.approved_review = Review.objects.create(
            user=self.regular_user,
            rating=5,
            comment='Great product!',
            content_type=self.content_type,
            object_id=self.product.id,
            approved=True
        )
        
        self.unapproved_review = Review.objects.create(
            user=self.regular_user,
            rating=4,
            comment='Good product',
            content_type=self.content_type,
            object_id=self.product.id,
            approved=False
        )
    
    def test_regular_user_sees_only_approved_reviews(self):
        """
        Test that regular users only see approved reviews in product data.
        
        This ensures that unapproved reviews are hidden from
        regular users for content moderation purposes.
        """
        # Create request context for regular user
        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.regular_user
        
        # Serialize product with regular user context
        serializer = BaseProductItemSerializer(
            self.product,
            context={'request': request}
        )
        data = serializer.data
        
        # Get reviews from serialized data
        reviews = data.get('review', [])
        
        # Should only see approved review
        self.assertEqual(len(reviews), 1)
        self.assertTrue(reviews[0]['approved'])
        self.assertEqual(reviews[0]['id'], self.approved_review.id)
    
    def test_reviewer_sees_all_reviews(self):
        """
        Test that reviewers see both approved and unapproved reviews.
        
        This ensures that reviewers can see all reviews for
        moderation purposes, including their own unapproved reviews.
        """
        # Create request context for reviewer user
        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.reviewer_user
        
        # Serialize product with reviewer user context
        serializer = BaseProductItemSerializer(
            self.product,
            context={'request': request}
        )
        data = serializer.data
        
        # Get reviews from serialized data
        reviews = data.get('review', [])
        
        # Should see both approved and unapproved reviews
        self.assertEqual(len(reviews), 2)
        
        # Check that both reviews are present
        review_ids = [review['id'] for review in reviews]
        self.assertIn(self.approved_review.id, review_ids)
        self.assertIn(self.unapproved_review.id, review_ids)
        
        # Check approval status
        approved_review = next(r for r in reviews if r['id'] == self.approved_review.id)
        unapproved_review = next(r for r in reviews if r['id'] == self.unapproved_review.id)
        
        self.assertTrue(approved_review['approved'])
        self.assertFalse(unapproved_review['approved'])
    
    def test_reviewer_sees_own_unapproved_review(self):
        """
        Test that a reviewer can see their own unapproved review.
        
        This is important for the workflow where a reviewer submits
        a review and needs to see it for approval purposes.
        """
        # Create an unapproved review by the reviewer
        reviewer_review = Review.objects.create(
            user=self.reviewer_user,
            rating=3,
            comment='My review',
            content_type=self.content_type,
            object_id=self.product.id,
            approved=False
        )
        
        # Create request context for reviewer user
        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.reviewer_user
        
        # Serialize product with reviewer user context
        serializer = BaseProductItemSerializer(
            self.product,
            context={'request': request}
        )
        data = serializer.data
        
        # Get reviews from serialized data
        reviews = data.get('review', [])
        
        # Should see all reviews including the reviewer's own unapproved review
        self.assertEqual(len(reviews), 3)
        
        # Check that the reviewer's review is present
        reviewer_review_data = next(
            (r for r in reviews if r['id'] == reviewer_review.id),
            None
        )
        self.assertIsNotNone(reviewer_review_data)
        self.assertFalse(reviewer_review_data['approved'])
        self.assertEqual(reviewer_review_data['user'], self.reviewer_user.id) 