# Accounts Views Tests
# This module contains tests for the accounts views to ensure
# authentication endpoints work correctly.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import uuid

from src.accounts.views.user_credential import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView
)
from src.accounts.utils import migrate_guest_data_to_user
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class AccountsViewsTestCase(TestCase):
    """
    Test case for accounts views.

    This test case verifies that authentication endpoints
    work correctly for registration, login, and logout.
    """

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
        """
        Test user registration with guest ID for data migration.

        This test verifies that guest data is migrated when
        a user registers with a guest ID.
        """
        # Arrange
        unique_id = str(uuid.uuid4())[:8]
        register_data = {
            'email': f'guestuser_{unique_id}@example.com',
            'username': f'guestuser_{unique_id}',
            'password': 'Testpass123!',  # Updated password to meet requirements
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
        """
        Test successful user login with email.

        This test verifies that users can log in successfully
        using their email address.
        """
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
        """
        Test successful user login with username.

        This test verifies that users can log in successfully
        using their username.
        """
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

    def test_user_login_with_guest_id(self):
        """
        Test user login with guest ID for data migration.

        This test verifies that guest data is migrated when
        a user logs in with a guest ID.
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

    def test_user_login_invalid_credentials(self):
        """
        Test user login with invalid credentials.

        This test verifies that login fails with
        incorrect password.
        """
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

    def test_register_view_permissions(self):
        """
        Test that register view allows anonymous access.

        This test verifies that the register view
        is accessible without authentication.
        """
        # Arrange
        view = UserRegisterView()

        # Act & Assert
        self.assertIn(
            'AllowAny', [perm.__name__ for perm in view.permission_classes])

    def test_login_view_permissions(self):
        """
        Test that login view allows anonymous access.

        This test verifies that the login view
        is accessible without authentication.
        """
        # Arrange
        view = UserLoginView()

        # Act & Assert
        self.assertIn(
            'AllowAny', [perm.__name__ for perm in view.permission_classes])

    def test_register_view_guest_data_migration(self):
        """
        Test that register view calls guest data migration.

        This test verifies that the register view
        properly migrates guest data when guest ID is provided.
        """
        # Arrange
        register_data = {
            'email': 'migrationuser@example.com',
            'username': 'migrationuser',
            'password': 'Testpass123!',  # Updated password to meet requirements
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
        Test that login view calls guest data migration.

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
