"""
This module defines serializers for user registration, login, logout, and password change operations.
"""

from typing import Any, cast
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from src.accounts.constants import UserErrorMessages
from src.accounts.validators.models import UsernameValidator, EmailOrUsernameValidator

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Inherits from ModelSerializer, which automatically generates fields based on the User model.
    Handles validation and creation of new user instances, including password hashing and email consent.
    """
    # Password field: write_only means it won't be returned in API responses.
    # trim_whitespace=False ensures passwords are not altered by removing spaces.
    password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False)
    # Consent field: write_only as it's only needed during registration.
    agreed_to_emails: serializers.BooleanField = serializers.BooleanField(
        write_only=True)

    class Meta:
        model: type[AbstractBaseUser] = UserModel
        # Fields to include in the API (must match model fields or serializer fields)
        fields: list[str] = [
            'email',
            'username',
            'password',
            'agreed_to_emails'
        ]

    def validate_password(self, value: str) -> str:
        validate_password(value)

        return value

    def validate_username(self, value: str) -> str:
        """
        Validate the username using a custom validator.
        Ensures the username meets project-specific requirements (e.g., allowed characters).
        """
        username_validator = UsernameValidator()
        username_validator(value)

        return value

    def validate_agreed_to_emails(self, value: bool) -> bool:
        """
        Ensure the user has agreed to receive email updates.
        """
        if not value:
            raise serializers.ValidationError(
                UserErrorMessages.AGREED_TO_EMAILS,
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> AbstractBaseUser:
        """
        Create a new user instance using the validated data.
        Uses the custom manager's create_user method, which handles password hashing and other logic.
        """
        user = UserModel.objects.create_user(**validated_data)
        return cast(AbstractBaseUser, user)


class UserLoginRequestSerializer(serializers.Serializer):
    """
    Serializer for user login requests.

    Uses a plain Serializer (not ModelSerializer) because login does not create or update model instances.
    Accepts either email or username and a password.
    """
    email_or_username: serializers.CharField = serializers.CharField()
    password: serializers.CharField = serializers.CharField()

    def validate_email_or_username(self, value: str) -> str:
        """
        Validate the email or username using a custom validator.
        Ensures the input is a valid email or username format.
        """
        email_or_username_validator = EmailOrUsernameValidator()
        email_or_username_validator(value)
        return value


class UserLoginResponseSerializer(serializers.Serializer):
    """
    Serializer for user login responses.

    Returns authentication tokens and a message after successful login.
    """
    refresh: serializers.CharField = serializers.CharField()
    access: serializers.CharField = serializers.CharField()
    message: serializers.CharField = serializers.CharField()


class UserLogoutRequestSerializer(serializers.Serializer):
    """
    Serializer for user logout requests.

    Accepts a refresh token to invalidate the session.
    """
    refresh: serializers.CharField = serializers.CharField()


class UserLogoutResponseSerializer(serializers.Serializer):
    """
    Serializer for user logout responses.

    Returns a message confirming logout.
    """
    message: serializers.CharField = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.

    Handles validation of current and new passwords.
    """
    current_password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False
    )
    new_password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False
    )

    def validate_current_password(self, value: str) -> str:
        """
        Ensure the current password matches the user's actual password.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                UserErrorMessages.INCORRECT_PASSWORD)
        return value

    def validate_new_password(self, value: str) -> str:
        """
        Validate the new password using Django's and custom password validators.
        """
        validate_password(value, user=self.context['request'].user)
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Object-level validation to ensure the new password is different from the current password.
        """
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {"new_password": UserErrorMessages.NEW_PASSWORD_SAME_AS_CURRENT}
            )
        return attrs

    def save(self) -> AbstractBaseUser:
        """
        Set the new password for the user and save the user instance.
        This method is called after validation passes.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        return user
