# Authentication Tests
# This module contains tests for the CustomAuthBackendBackend to ensure
# authentication works correctly with both email and username login methods.

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser

from src.accounts.authentication import CustomAuthBackendBackend
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class CustomAuthBackendBackendTestCase(TestCase):
    """
    Test case for CustomAuthBackendBackend.
    
    This test case verifies that the custom authentication backend
    correctly handles authentication with both email and username.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data for all test methods in this class.
        """
        cls.backend = CustomAuthBackendBackend()
        cls.factory = RequestFactory()
    
    def setUp(self):
        """
        Set up test-specific data for each test method.
        """
        # Create test user
        self.user = TestDataBuilder.create_authenticated_user('testuser', 'testuser')
        self.user.set_password('testpass123')
        self.user.save()
    
    def test_authenticate_with_email_success(self):
        """
        Test authentication with email address.
        
        This test verifies that users can authenticate using their
        email address as the login identifier.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
        self.assertEqual(authenticated_user.email, self.user.email)
    
    def test_authenticate_with_username_success(self):
        """
        Test authentication with username.
        
        This test verifies that users can authenticate using their
        username as the login identifier.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.username,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
        self.assertEqual(authenticated_user.username, self.user.username)
    
    def test_authenticate_with_email_case_insensitive(self):
        """
        Test authentication with email case insensitive.
        
        This test verifies that email authentication is case insensitive,
        allowing users to log in regardless of email case.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        mixed_case_email = self.user.email.upper()
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=mixed_case_email,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
    
    def test_authenticate_with_username_case_insensitive(self):
        """
        Test authentication with username case insensitive.
        
        This test verifies that username authentication is case insensitive,
        allowing users to log in regardless of username case.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        mixed_case_username = self.user.username.upper()
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=mixed_case_username,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
    
    def test_authenticate_with_invalid_email(self):
        """
        Test authentication with non-existent email.
        
        This test verifies that authentication fails when
        an email address doesn't exist in the database.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username='nonexistent@example.com',
            password='testpass123'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_invalid_username(self):
        """
        Test authentication with non-existent username.
        
        This test verifies that authentication fails when
        a username doesn't exist in the database.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username='nonexistentuser',
            password='testpass123'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_wrong_password(self):
        """
        Test authentication with correct email but wrong password.
        
        This test verifies that authentication fails when
        the password is incorrect, even with a valid email.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password='wrongpassword'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_inactive_user(self):
        """
        Test authentication with inactive user.
        
        This test verifies that inactive users cannot authenticate,
        even with correct credentials.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        self.user.is_active = False
        self.user.save()
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_empty_username(self):
        """
        Test authentication with empty username.
        
        This test verifies that authentication fails when
        no username/email is provided.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username='',
            password='testpass123'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_none_username(self):
        """
        Test authentication with None username.
        
        This test verifies that authentication fails when
        username is None.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=None,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_empty_password(self):
        """
        Test authentication with empty password.
        
        This test verifies that authentication fails when
        password is empty.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password=''
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_none_password(self):
        """
        Test authentication with None password.
        
        This test verifies that authentication fails when
        password is None.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password=None
        )
        
        # Assert
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_with_no_request(self):
        """
        Test authentication without request object.
        
        This test verifies that authentication works correctly
        when no request object is provided.
        """
        # Act
        authenticated_user = self.backend.authenticate(
            request=None,
            username=self.user.email,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
    
    def test_backend_inheritance(self):
        """
        Test that the backend properly inherits from ModelBackend.
        
        This test verifies that our custom backend maintains
        compatibility with Django's authentication system.
        """
        # Assert
        self.assertIsInstance(self.backend, ModelBackend)
        self.assertIsInstance(self.backend, CustomAuthBackendBackend)
    
    def test_authenticate_with_additional_kwargs(self):
        """
        Test authentication with additional keyword arguments.
        
        This test verifies that the backend handles additional
        keyword arguments gracefully.
        """
        # Arrange
        request = self.factory.get('/api/login/')
        
        # Act
        authenticated_user = self.backend.authenticate(
            request=request,
            username=self.user.email,
            password='testpass123',
            extra_param='should_be_ignored'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
    
    def test_authenticate_with_django_authenticate_function(self):
        """
        Test authentication using Django's authenticate function.
        
        This test verifies that our custom backend works correctly
        when used with Django's built-in authenticate function.
        """
        # Act
        authenticated_user = authenticate(
            username=self.user.email,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)
    
    def test_authenticate_with_username_via_django_authenticate(self):
        """
        Test authentication with username using Django's authenticate function.
        
        This test verifies that our custom backend works correctly
        with usernames when used with Django's authenticate function.
        """
        # Act
        authenticated_user = authenticate(
            username=self.user.username,
            password='testpass123'
        )
        
        # Assert
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user) 