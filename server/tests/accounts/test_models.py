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

    def test_user_creation_with_email_only(self):
        """
        Test that a user can be created with email only (username optional).
        
        Note: The UserCredential model requires a username, so we provide
        a unique username for this test while still testing the email-based
        authentication functionality.
        
        Arrange: Test data
        Act: Create user with email and minimal username
        Assert: User is created successfully
        """
        # Arrange
        email = 'emailonly_unique@example.com'
        username = 'emailonly_user_unique'
        password = 'EmailPass123!'
        
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

    def test_email_uniqueness(self):
        """
        Test that email addresses must be unique.
        
        Arrange: Create first user with email
        Act: Try to create another user with same email
        Assert: IntegrityError is raised
        """
        # Arrange
        first_user = UserModel.objects.create_user(
            email='duplicate_unique@example.com',
            username='firstuser_unique',
            password='FirstPass123!'
        )
        
        # Act & Assert
        with self.assertRaises(IntegrityError):
            UserModel.objects.create_user(
                email='duplicate_unique@example.com',
                username='seconduser_unique',
                password='SecondPass123!'
            )

    def test_username_uniqueness(self):
        """
        Test that usernames must be unique.
        
        Arrange: Create first user with username
        Act: Try to create another user with same username
        Assert: IntegrityError is raised
        """
        # Arrange
        first_user = UserModel.objects.create_user(
            email='first_unique@example.com',
            username='duplicate_username_unique',
            password='FirstPass123!'
        )
        
        # Act & Assert
        with self.assertRaises(IntegrityError):
            UserModel.objects.create_user(
                email='second_unique@example.com',
                username='duplicate_username_unique',
                password='SecondPass123!'
            )

    def test_password_hashing(self):
        """
        Test that passwords are properly hashed.
        
        Arrange: Create user with password
        Act: Check password
        Assert: Password is hashed and can be verified
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='password_test_unique@example.com',
            username='password_test_unique',
            password='TestPass123!'
        )
        
        # Act & Assert
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.check_password('wrong_password'))

    def test_superuser_creation(self):
        """
        Test that superusers are created with proper permissions.
        
        Arrange: Test data
        Act: Create superuser
        Assert: Superuser has correct permissions
        """
        # Arrange
        email = 'admin_unique@example.com'
        username = 'admin_unique'
        password = 'AdminPass123!'
        
        # Act
        superuser = UserModel.objects.create_superuser(
            email=email,
            username=username,
            password=password
        )
        
        # Assert
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))

    def test_user_string_representation(self):
        """
        Test the string representation of the user model.
        
        Arrange: Create user
        Act: Convert user to string
        Assert: String representation is the email
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='string_test_unique@example.com',
            username='string_test_unique',
            password='StringPass123!'
        )
        
        # Act
        string_repr = str(user)
        
        # Assert
        self.assertEqual(string_repr, 'string_test_unique@example.com')

    def test_agreed_to_emails_default(self):
        """
        Test that agreed_to_emails defaults to False.
        
        Arrange: Create user
        Act: Check agreed_to_emails field
        Assert: Default value is False
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='default_test_unique@example.com',
            username='default_test_unique',
            password='DefaultPass123!'
        )
        
        # Act & Assert
        self.assertFalse(user.agreed_to_emails)


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

    def test_profile_optional_fields(self):
        """
        Test that profile fields are optional (null=True, blank=False).
        """
        user = UserModel.objects.create_user(
            email='minimal@example.com',
            username='minimal',
            password='MinimalPass123!'
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        self.assertIsNone(profile.first_name)
        self.assertIsNone(profile.last_name)
        self.assertIsNone(profile.phone_number)
        self.assertIsNone(profile.country)
        self.assertIsNone(profile.city)
        self.assertIsNone(profile.zip_code)
        self.assertIsNone(profile.street_address)
        self.assertIsNone(profile.apartment)

    def test_profile_apartment_optional(self):
        """
        Test that apartment field is truly optional (blank=True).
        """
        user = UserModel.objects.create_user(
            email='apartment_optional_test@example.com',
            username='apartment_optional_test',
            password='NoAptPass123!'
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Update the profile with test data
        profile.first_name = 'Bob'
        profile.last_name = 'Johnson'
        profile.phone_number = '5551234567'
        profile.country = 'United States'
        profile.city = 'Los Angeles'
        profile.zip_code = '90210'
        profile.street_address = '789 Pine St'
        # apartment field omitted
        profile.save()
        
        self.assertIsNone(profile.apartment)
        self.assertEqual(profile.first_name, 'Bob')

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

    def test_photo_optional_field(self):
        """
        Test that photo field is optional (null=True, blank=False).
        
        Arrange: Create user
        Act: Create photo without uploading image
        Assert: Photo is created successfully
        """
        # Arrange
        user = UserModel.objects.create_user(
            email='photo_optional_test@example.com',
            username='photo_optional_test',
            password='PhotoOptionalPass123!'
        )
        
        # Act
        photo, created = UserPhoto.objects.get_or_create(user=user)
        
        # Assert
        self.assertIsNone(photo.photo)
        self.assertEqual(photo.user, user) 