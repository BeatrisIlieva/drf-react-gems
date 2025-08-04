"""
This module defines serializers for user registration, login, logout, and password change operations.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import serializers

from src.common.tasks import _send_email

from src.accounts.constants import UserErrorMessages
from src.accounts.validators.models import (
    UsernameValidator,
    EmailOrUsernameValidator,
)

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Inherits from ModelSerializer, which automatically generates fields based on the User model.
    Handles validation and creation of new user instances, including password hashing and email consent.
    """

    # Password field: write_only means it won't be returned in API responses.
    # trim_whitespace=False ensures passwords are not altered by removing spaces.
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    # Consent field: write_only as it's only needed during registration.
    agreed_to_emails = serializers.BooleanField(write_only=True)

    class Meta:
        model = UserModel
        # Fields to include in the API (must match model fields or serializer fields)
        fields = [
            'email',
            'username',
            'password',
            'agreed_to_emails',
        ]

    def validate_password(self, value):
        validate_password(value)

        return value

    def validate_username(self, value):
        """
        Validate the username using a custom validator.
        Ensures the username meets project-specific requirements (e.g., allowed characters).
        """
        username_validator = UsernameValidator()

        username_validator(value)

        return value

    def validate_agreed_to_emails(self, value):
        """
        Ensure the user has agreed to receive email updates.
        """
        if not value:
            raise serializers.ValidationError(
                UserErrorMessages.AGREED_TO_EMAILS
            )

        return value

    def create(self, validated_data):
        """
        Create a new user instance using the validated data.
        Uses the custom manager's create_user method, which handles password hashing and other logic.
        """
        user = UserModel.objects.create_user(**validated_data)

        return user


class UserLoginRequestSerializer(serializers.Serializer):
    """
    Serializer for user login requests.

    Uses a plain Serializer (not ModelSerializer) because login does not create or update model instances.
    Accepts either email or username and a password.
    """

    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate_email_or_username(self, value):
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

    refresh = serializers.CharField()
    access = serializers.CharField()
    message = serializers.CharField()


class UserLogoutRequestSerializer(serializers.Serializer):
    """
    Serializer for user logout requests.

    Accepts a refresh token to invalidate the session.
    """

    refresh = serializers.CharField()


class UserLogoutResponseSerializer(serializers.Serializer):
    """
    Serializer for user logout responses.

    Returns a message confirming logout.
    """

    message = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.

    Handles validation of current and new passwords.
    """

    current_password = serializers.CharField(
        write_only=True, trim_whitespace=False
    )
    new_password = serializers.CharField(
        write_only=True, trim_whitespace=False
    )

    def validate_current_password(self, value):
        """
        Ensure the current password matches the user's actual password.
        """
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                UserErrorMessages.INCORRECT_PASSWORD
            )

        return value

    def validate_new_password(self, value):
        """
        Validate the new password using Django's and custom password validators.
        """
        validate_password(value, user=self.context['request'].user)

        return value

    def validate(self, attrs):
        """
        Object-level validation to ensure the new password is different from the current password.
        """
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {
                    'new_password': UserErrorMessages.NEW_PASSWORD_SAME_AS_CURRENT
                }
            )

        return attrs

    def save(self):
        """
        Set the new password for the user and save the user instance.
        This method is called after validation passes.
        """
        user = self.context['request'].user

        user.set_password(self.validated_data['new_password'])

        user.save()

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        email = self.validated_data['email']

        try:
            user = UserModel.objects.get(email=email, is_active=True)

            # converts 123 to something like MTIz
            # It's reversible -> we can decode it to get the user ID back
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Creates secure tokens tied to the user
            token = default_token_generator.make_token(user)

            # Reset URL to provide into the email
            reset_url = f'{settings.FRONTEND_URL}/reset-password/{uid}/{token}'

            # Send email
            html_message = render_to_string(
                'mailer/reset-password.html', {'reset_url': reset_url}
            )
            plain_message = strip_tags(html_message)

            _send_email.delay(
                subject='Reset Password',
                message=plain_message,
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=(user.email,),
            )

        except UserModel.DoesNotExist:
            pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    # Fields expected from the frontend
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = attrs['uid']
            token = attrs['token']

            # Decode the UID to get the original user ID (e.g., from MTIz to 123)
            user_id = force_str(urlsafe_base64_decode(uid))

            # Try to fetch the user with the decoded ID
            user = UserModel.objects.get(pk=user_id)

            # Check if the token is valid for this user
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError(
                    UserErrorMessages.INVALID_TOKEN
                )

            # Store the user in validated_data so we can use it in save()
            attrs['user'] = user

            return attrs

        # Handle cases where UID is invalid or user doesn't exist
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise serializers.ValidationError(UserErrorMessages.INVALID_TOKEN)

    def save(self):
        # Get user and new password from validated data
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        html_message = render_to_string(
            'mailer/password-has-been-reset.html',
        )

        plain_message = strip_tags(html_message)

        _send_email.delay(
            subject='Your password has been reset',
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(user.email,),
        )
