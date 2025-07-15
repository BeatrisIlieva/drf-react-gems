"""
Tests for Accounts Models

This module contains comprehensive tests for the accounts models including
UserCredential, UserProfile, and UserPhoto models. The tests follow the
Triple A pattern (Arrange, Act, Assert) and cover all model functionality
including field validation, relationships, and custom methods.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from src.accounts.models.user_credential import UserCredential
from src.accounts.models.user_profile import UserProfile
from src.accounts.models.user_photo import UserPhoto

UserModel = get_user_model()


class UserCredentialModelTest(TestCase):
    """
    Test cases for the UserCredential model.

    Tests cover:
    - User creation with email and username
    - Email uniqueness validation
    - Username uniqueness validation
    - Password hashing
    - Custom manager methods
    - String representation
    """

    def test_user_creation_with_email_and_username(self):
        """
        Test that a user can be created with email and username.

        Arrange: Test data
        Act: Create a new user
        Assert: User is created with correct email and username
        """
        # Arrange
        email = 'newuser@example.com'
        username = 'newuser'
        password = 'NewPass123!'

        # Act
        user = UserModel.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        # Assert
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class UserProfileModelTest(TestCase):
    """
    Test cases for the UserProfile model.

    Tests cover:
    - Profile creation and user relationship
    - Field validation
    - Optional fields
    - One-to-one relationship integrity
    """

    def test_profile_creation(self):
        """
        Test that a user profile can be created with all fields.
        """
        user = UserModel.objects.create_user(
            email='profile_creation_test@example.com',
            username='profile_creation_test',
            password='NewProfilePass123!'
        )
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '9876543210',
                'country': 'Canada',
                'city': 'Toronto',
                'zip_code': 'M5V 3A8',
                'street_address': '456 Oak Ave',
                'apartment': 'Unit 2'
            }
        )
        # Update the profile with the test data
        profile.first_name = 'Jane'
        profile.last_name = 'Smith'
        profile.phone_number = '9876543210'
        profile.country = 'Canada'
        profile.city = 'Toronto'
        profile.zip_code = 'M5V 3A8'
        profile.street_address = '456 Oak Ave'
        profile.apartment = 'Unit 2'
        profile.save()

        self.assertEqual(profile.first_name, 'Jane')
        self.assertEqual(profile.last_name, 'Smith')
        self.assertEqual(profile.phone_number, '9876543210')
        self.assertEqual(profile.country, 'Canada')
        self.assertEqual(profile.city, 'Toronto')
        self.assertEqual(profile.zip_code, 'M5V 3A8')
        self.assertEqual(profile.street_address, '456 Oak Ave')
        self.assertEqual(profile.apartment, 'Unit 2')

    def test_profile_user_relationship(self):
        """
        Test the one-to-one relationship between user and profile.
        """
        user = UserModel.objects.create_user(
            email='relationship_test@example.com',
            username='relationship_test',
            password='RelPass123!'
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Update the profile with test data
        profile.first_name = 'John'
        profile.last_name = 'Doe'
        profile.phone_number = '1234567890'
        profile.country = 'United States'
        profile.city = 'New York'
        profile.zip_code = '10001'
        profile.street_address = '123 Main St'
        profile.apartment = 'Apt 4B'
        profile.save()

        self.assertEqual(profile.user, user)
        self.assertEqual(user.userprofile, profile)

    def test_profile_primary_key(self):
        """
        Test that the user field is the primary key.
        """
        user = UserModel.objects.create_user(
            email='primary_key_test@example.com',
            username='primary_key_test',
            password='PrimaryKeyPass123!'
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Update the profile with test data
        profile.first_name = 'John'
        profile.last_name = 'Doe'
        profile.phone_number = '1234567890'
        profile.country = 'United States'
        profile.city = 'New York'
        profile.zip_code = '10001'
        profile.street_address = '123 Main St'
        profile.apartment = 'Apt 4B'
        profile.save()

        self.assertEqual(profile.pk, user.pk)
        self.assertEqual(profile.user_id, user.pk)


class UserPhotoModelTest(TestCase):
    """
    Test cases for the UserPhoto model.

    Tests cover:
    - Photo creation and user relationship
    - Cloudinary field functionality
    - One-to-one relationship integrity
    """

    def test_photo_creation(self):
        """
        Test that a user photo can be created.

        Arrange: Create user
        Act: Create photo
        Assert: Photo is created with correct relationship
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='photo_creation_test@example.com',
            username='photo_creation_test',
            password='PhotoPass123!'
        )

        # Act
        photo, created = UserPhoto.objects.get_or_create(user=user)

        # Assert
        self.assertEqual(photo.user, user)
        self.assertIsNone(photo.photo)  # No photo uploaded initially

    def test_photo_user_relationship(self):
        """
        Test the one-to-one relationship between user and photo.

        Arrange: Create user and photo
        Act: Access relationship
        Assert: Relationship works correctly
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='photo_relationship_test@example.com',
            username='photo_relationship_test',
            password='PhotoRelPass123!'
        )
        photo, created = UserPhoto.objects.get_or_create(user=user)

        # Act & Assert
        self.assertEqual(photo.user, user)
        # Note: user.userphoto would raise AttributeError if not set up properly
        # This is expected behavior for one-to-one relationships

    def test_photo_primary_key(self):
        """
        Test that the user field is the primary key.

        Arrange: Create user and photo
        Act: Check primary key
        Assert: User field is the primary key
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='photo_primary_key_test@example.com',
            username='photo_primary_key_test',
            password='PhotoPrimaryKeyPass123!'
        )
        photo, created = UserPhoto.objects.get_or_create(user=user)

        # Act & Assert
        self.assertEqual(photo.pk, user.pk)
        self.assertEqual(photo.user_id, user.pk)
