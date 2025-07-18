from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
import uuid

from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class AccountsViewsTestCase(TestCase):

    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create guest ID for testing
        self.guest_id = TestDataBuilder.create_guest_id()

        # Create test user
        self.user = TestDataBuilder.create_authenticated_user(
            'testuser', 'testuser')
        self.user.set_password('testpass123')
        self.user.save()

    def test_user_register_with_guest_id(self):
        # Arrange
        unique_id = str(uuid.uuid4())[:8]
        register_data = {
            'email': f'guestuser_{unique_id}@example.com',
            'username': f'guestuser_{unique_id}',
            'password': 'Testpass123!',
            'agreed_to_emails': True
        }

        # Act
        response = self.client.post(
            reverse('register'),
            register_data,
            headers={'Guest-Id': str(self.guest_id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_user_login_success_with_email(self):
        # Arrange
        login_data = {
            'email_or_username': self.user.email,
            'password': 'testpass123'
        }

        # Act
        response = self.client.post(reverse('login'), login_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('message', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('id', response.data)

    def test_user_login_success_with_username(self):
        # Arrange
        login_data = {
            'email_or_username': self.user.username,
            'password': 'testpass123'
        }

        # Act
        response = self.client.post(reverse('login'), login_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('message', response.data)

    def test_user_login_invalid_credentials(self):
        # Arrange
        invalid_data = {
            'email_or_username': self.user.email,
            'password': 'wrongpassword'
        }

        # Act
        response = self.client.post(reverse('login'), invalid_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_register_view_guest_data_migration(self):
        """
        This test verifies that the register view
        properly migrates guest data when guest ID is provided.
        """
        # Arrange
        register_data = {
            'email': 'migrationuser@example.com',
            'username': 'migrationuser',
            'password': 'Testpass123!',
            'agreed_to_emails': True
        }

        # Act
        response = self.client.post(
            reverse('register'),
            register_data,
            headers={'Guest-Id': str(self.guest_id)}
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify user was created
        user = UserModel.objects.get(email='migrationuser@example.com')
        self.assertIsNotNone(user)

    def test_login_view_guest_data_migration(self):
        """
        This test verifies that the login view
        properly migrates guest data when guest ID is provided.
        """
        # Arrange
        login_data = {
            'email_or_username': self.user.email,
            'password': 'testpass123'
        }

        # Act
        response = self.client.post(
            reverse('login'),
            login_data,
            headers={'Guest-Id': str(self.guest_id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
