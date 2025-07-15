"""
Tests for Common Services

This module contains comprehensive tests for the common services including
UserIdentificationService. The tests follow the Triple A pattern (Arrange, Act, Assert)
and cover all service functionality including user identification for both
authenticated and guest users.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
import uuid

from src.common.services import UserIdentificationService

UserModel = get_user_model()


class UserIdentificationServiceTest(TestCase):
    """
    Test cases for the UserIdentificationService class.

    Tests cover:
    - Authenticated user identification
    - Guest user identification with valid UUID
    - Guest user identification with missing header
    - Guest user identification with invalid UUID format
    - Error handling for various scenarios
    """

    def setUp(self):
        """
        Set up test data for each test method.

        Creates test users and request factory for testing
        user identification functionality.
        """
        self.factory = APIRequestFactory()

        # Create test user
        self.test_user = UserModel.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )

        # Create valid guest ID for testing
        self.valid_guest_id = str(uuid.uuid4())

    def test_get_user_identifier_authenticated_user(self):
        """
        Test user identification for authenticated users.

        Arrange: Create request with authenticated user
        Act: Call get_user_identifier method
        Assert: Returns user object in dictionary
        """
        # Arrange
        request = self.factory.get('/test/')
        request.user = self.test_user

        # Act
        result = UserIdentificationService.get_user_identifier(request)

        # Assert
        self.assertIn('user', result)
        self.assertEqual(result['user'], self.test_user)
        self.assertNotIn('guest_id', result)

    def test_get_user_identifier_guest_user_valid_uuid(self):
        """
        Test user identification for guest users with valid UUID.

        Arrange: Create request with Guest-Id header containing valid UUID
        Act: Call get_user_identifier method
        Assert: Returns guest_id in dictionary
        """
        # Arrange
        request = self.factory.get('/test/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        request.headers = {'Guest-Id': self.valid_guest_id}

        # Act
        result = UserIdentificationService.get_user_identifier(request)

        # Assert
        self.assertIn('guest_id', result)
        self.assertEqual(str(result['guest_id']), self.valid_guest_id)
        self.assertNotIn('user', result)

    def test_get_user_identifier_guest_user_missing_header(self):
        """
        Test user identification for guest users without Guest-Id header.

        Arrange: Create request with anonymous user but no Guest-Id header
        Act: Call get_user_identifier method
        Assert: Raises ValidationError
        """
        # Arrange
        request = self.factory.get('/test/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        request.headers = {}

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            UserIdentificationService.get_user_identifier(request)

        # Check the error message
        self.assertIn('guest_id', context.exception.detail)
        self.assertIn('Guest-Id header is required',
                      str(context.exception.detail))

    def test_get_user_identifier_guest_user_invalid_uuid_format(self):
        """
        Test user identification for guest users with invalid UUID format.

        Arrange: Create request with Guest-Id header containing invalid UUID
        Act: Call get_user_identifier method
        Assert: Raises ValidationError
        """
        # Arrange
        request = self.factory.get('/test/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        request.headers = {'Guest-Id': 'invalid-uuid-format'}

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            UserIdentificationService.get_user_identifier(request)

        # Check the error message
        self.assertIn('guest_id', context.exception.detail)
        self.assertIn('Invalid guest ID format', str(context.exception.detail))

    def test_get_user_identifier_guest_user_empty_uuid(self):
        """
        Test user identification for guest users with empty UUID.

        Arrange: Create request with Guest-Id header containing empty string
        Act: Call get_user_identifier method
        Assert: Raises ValidationError
        """
        # Arrange
        request = self.factory.get('/test/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        request.headers = {'Guest-Id': ''}

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            UserIdentificationService.get_user_identifier(request)

        # Check the error message - empty string is treated as missing header
        self.assertIn('guest_id', context.exception.detail)
        self.assertIn('Guest-Id header is required',
                      str(context.exception.detail))

    def test_get_user_identifier_authenticated_user_consistency(self):
        """
        Test that authenticated user identification returns consistent results.

        Arrange: Create multiple requests with same authenticated user
        Act: Call get_user_identifier method multiple times
        Assert: All return same user object
        """
        # Arrange
        requests = []
        for _ in range(3):
            request = self.factory.get('/test/')
            request.user = self.test_user
            requests.append(request)

        # Act
        results = []
        for request in requests:
            result = UserIdentificationService.get_user_identifier(request)
            results.append(result)

        # Assert
        for result in results:
            self.assertIn('user', result)
            self.assertEqual(result['user'], self.test_user)

        # All results should be identical
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])
