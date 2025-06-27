from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from src.accounts.validators.models import UsernameValidator, EmailOrUsernameValidator
from src.accounts.serializers import UserRegisterSerializer, UserLoginRequestSerializer

UserModel = get_user_model()


class UsernameValidatorTest(TestCase):
    def setUp(self):
        self.validator = UsernameValidator()

    def test_valid_username(self):
        """Test that valid usernames pass validation"""
        valid_usernames = [
            'user123',
            'test_user',
            'admin',
            'user_123_test',
            'USERNAME',
            'a' * 30  # 30 characters (max)
        ]
        
        for username in valid_usernames:
            with self.subTest(username=username):
                try:
                    self.validator(username)
                except ValidationError:
                    self.fail(f"Valid username {username} should not raise ValidationError")

    def test_invalid_username(self):
        """Test that invalid usernames raise ValidationError"""
        invalid_usernames = [
            'ab',  # too short
            'a' * 31,  # too long
            'user-name',  # contains hyphen
            'user name',  # contains space
            'user@name',  # contains special character
            'user.name',  # contains dot
            '',  # empty
            'user#123'  # contains hash
        ]
        
        for username in invalid_usernames:
            with self.subTest(username=username):
                with self.assertRaises(ValidationError):
                    self.validator(username)


class EmailOrUsernameValidatorTest(TestCase):
    def setUp(self):
        self.validator = EmailOrUsernameValidator()

    def test_valid_email_or_username(self):
        """Test that valid emails and usernames pass validation"""
        valid_values = [
            # Valid emails
            'test@example.com',
            'user123@test.org',
            # Valid usernames
            'user123',
            'test_user',
            'admin',
            'USERNAME'
        ]
        
        for value in valid_values:
            with self.subTest(value=value):
                try:
                    self.validator(value)
                except ValidationError:
                    self.fail(f"Valid value {value} should not raise ValidationError")

    def test_invalid_email_or_username(self):
        """Test that invalid emails and usernames raise ValidationError"""
        invalid_values = [
            'ab',  # too short for username
            'invalid@',  # invalid email
            'user-name',  # invalid username (hyphen)
            'test@@example.com',  # invalid email
            '',  # empty
            'user name',  # invalid username (space)
        ]
        
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    self.validator(value)


class UserRegisterSerializerTest(TestCase):
    def test_valid_registration_data(self):
        """Test that valid registration data passes serializer validation"""
        valid_data = {
            'email': 'test@example.com',
            'username': 'testuser123',
            'password': 'TestPassword123!'
        }
        
        serializer = UserRegisterSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")

    def test_invalid_email_registration(self):
        """Test that invalid email fails serializer validation"""
        invalid_data = {
            'email': 'invalid@',
            'username': 'testuser123',
            'password': 'TestPassword123!'
        }
        
        serializer = UserRegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_username_registration(self):
        """Test that invalid username fails serializer validation"""
        invalid_data = {
            'email': 'test@example.com',
            'username': 'ab',  # too short
            'password': 'TestPassword123!'
        }
        
        serializer = UserRegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)


class UserLoginRequestSerializerTest(TestCase):
    def test_valid_login_email(self):
        """Test that valid email passes login serializer validation"""
        valid_data = {
            'email_or_username': 'test@example.com',
            'password': 'TestPassword123!'
        }
        
        serializer = UserLoginRequestSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")

    def test_valid_login_username(self):
        """Test that valid username passes login serializer validation"""
        valid_data = {
            'email_or_username': 'testuser123',
            'password': 'TestPassword123!'
        }
        
        serializer = UserLoginRequestSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")

    def test_invalid_login_credential(self):
        """Test that invalid email/username fails login serializer validation"""
        invalid_data = {
            'email_or_username': 'ab',  # too short for username, invalid email
            'password': 'TestPassword123!'
        }
        
        serializer = UserLoginRequestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email_or_username', serializer.errors)


class AuthenticationAPITest(APITestCase):
    def test_register_with_valid_data(self):
        """Test user registration with valid data"""
        data = {
            'email': 'test@example.com',
            'username': 'testuser123',
            'password': 'TestPassword123!'
        }
        
        response = self.client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_with_invalid_email(self):
        """Test user registration with invalid email"""
        data = {
            'email': 'invalid@',
            'username': 'testuser123',
            'password': 'TestPassword123!'
        }
        
        response = self.client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_username(self):
        """Test user registration with invalid username"""
        data = {
            'email': 'test@example.com',
            'username': 'ab',  # too short
            'password': 'TestPassword123!'
        }
        
        response = self.client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_credential(self):
        """Test login with invalid email/username format"""
        data = {
            'email_or_username': 'ab',  # invalid format
            'password': 'TestPassword123!'
        }
        
        response = self.client.post('/accounts/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
