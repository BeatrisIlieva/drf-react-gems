from typing import Any, Dict, Type, cast
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from src.accounts.validators.models import UsernameValidator, EmailOrUsernameValidator


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False)
    agreed_to_emails: serializers.BooleanField = serializers.BooleanField(
        write_only=True)

    class Meta:
        model: Type[AbstractBaseUser] = UserModel
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
        username_validator = UsernameValidator()
        username_validator(value)

        return value

    def validate_agreed_to_emails(self, value: bool) -> bool:
        if not value:
            raise serializers.ValidationError(
                "You must agree to receive email updates."
            )

        return value

    def create(self, validated_data: Dict[str, Any]) -> AbstractBaseUser:
        user = UserModel.objects.create_user(**validated_data)

        return cast(AbstractBaseUser, user)


class UserLoginRequestSerializer(serializers.Serializer):
    email_or_username: serializers.CharField = serializers.CharField()
    password: serializers.CharField = serializers.CharField()

    def validate_email_or_username(self, value: str) -> str:
        email_or_username_validator = EmailOrUsernameValidator()
        email_or_username_validator(value)

        return value


class UserLoginResponseSerializer(serializers.Serializer):
    refresh: serializers.CharField = serializers.CharField()
    access: serializers.CharField = serializers.CharField()
    message: serializers.CharField = serializers.CharField()


class UserLogoutRequestSerializer(serializers.Serializer):
    refresh: serializers.CharField = serializers.CharField()


class UserLogoutResponseSerializer(serializers.Serializer):
    message: serializers.CharField = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    current_password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False
    )
    new_password: serializers.CharField = serializers.CharField(
        write_only=True, trim_whitespace=False
    )

    def validate_current_password(self, value: str) -> str:
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")

        return value

    def validate_new_password(self, value: str) -> str:
        validate_password(value, user=self.context['request'].user)

        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from current password."}
            )
        return attrs

    def save(self) -> AbstractBaseUser:
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        return user
