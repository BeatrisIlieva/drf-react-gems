from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from src.accounts.authentication import CustomAuthBackendBackend
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class CustomAuthBackendBackendTestCase(TestCase):
    
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
        self.user = TestDataBuilder.create_authenticated_user(
            'testuser', 'testuser')
        self.user.set_password('testpass123')
        self.user.save()

    def test_authenticate_with_email_success(self):
        """
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

    def test_authenticate_with_invalid_email(self):
        """
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

    def test_authenticate_with_empty_username(self):
        """
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

    def test_authenticate_with_empty_password(self):
        """
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
