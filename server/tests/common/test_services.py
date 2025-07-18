from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
import uuid

from src.common.services import UserIdentificationService

UserModel = get_user_model()


class UserIdentificationServiceTest(TestCase):

    def setUp(self):
        """
        Creates test users and request factory for testing
        user identification functionality.
        """
        self.factory = APIRequestFactory(
        )  # specifically designed for testing DRF views and APIs; supports all request methods

        # Create test user
        self.test_user = UserModel.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )

        # Create valid guest ID for testing
        self.valid_guest_id = str(uuid.uuid4())

    def test_get_user_identifier_authenticated_user(self):
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
        # Arrange
        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        request.headers = {'Guest-Id': self.valid_guest_id}

        # Act
        result = UserIdentificationService.get_user_identifier(request)

        # Assert
        self.assertIn('guest_id', result)
        self.assertEqual(str(result['guest_id']), self.valid_guest_id)
        self.assertNotIn('user', result)

    def test_get_user_identifier_guest_user_missing_header(self):
        # Arrange
        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        request.headers = {}

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            UserIdentificationService.get_user_identifier(request)

        self.assertIn('guest_id', context.exception.detail)
        self.assertIn('Guest-Id header is required',
                      str(context.exception.detail))
