from django.test import TestCase
from django.contrib.auth import get_user_model


from src.accounts.models.user_profile import UserProfile
from src.accounts.models.user_photo import UserPhoto

UserModel = get_user_model()


class UserCredentialModelTest(TestCase):

    def test_user_creation_with_email_and_username(self):
        """
        Test that a user can be created with email and username.
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

    def test_profile_creation(self):
        """
        Test the one-to-one relationship between user and profile.
        """
        user = UserModel.objects.create_user(
            email='relationship_test@example.com',
            username='relationship_test',
            password='RelPass123!'
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
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
        self.assertEqual(profile.pk, user.pk)


class UserPhotoModelTest(TestCase):

    def test_photo_creation(self):
        # Arrange
        user = UserModel.objects.create_user(
            email='photo_creation_test@example.com',
            username='photo_creation_test',
            password='PhotoPass123!'
        )

        # Act
        photo, _ = UserPhoto.objects.get_or_create(user=user)

        # Assert
        self.assertEqual(photo.user, user)
        self.assertEqual(photo.pk, user.pk)
