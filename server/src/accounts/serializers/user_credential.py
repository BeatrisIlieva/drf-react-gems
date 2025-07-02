from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


from src.accounts.validators.models import UsernameValidator, EmailOrUsernameValidator


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    # when we create a user, in the response the hash password is sent
    # to resolve the problem we set the password to be write-only
    # write-only ensures that the password will not be returned in the response
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = UserModel
        # the serializer expects to receive json file containing `email`, `username` and `password`
        fields = ['email', 'username', 'password']

    def validate_password(self, value):
        # This will raise a ValidationError if the password is too short, common, numeric, etc.
        validate_password(value)
        return value

    def validate_username(self, value):
        # Validate username format using custom validator
        username_validator = UsernameValidator()
        username_validator(value)
        return value

    # the default `create` method does not hash the password
    # that's why we override the `create` method to call `create_user`
    # which hashes the password
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserLoginRequestSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate_email_or_username(self, value):
        # Validate that the value is either a valid email or username
        email_or_username_validator = EmailOrUsernameValidator()
        email_or_username_validator(value)
        return value

    # returns `accessToken` and `refreshToken`


class UserLoginResponseSerializer(serializers.Serializer):
    # returns `accessToken`, `refreshToken` and message
    refresh = serializers.CharField()
    access = serializers.CharField()
    message = serializers.CharField()


class UserLogoutRequestSerializer(serializers.Serializer):
    # upon logout we need to blacklist the refresh token
    refresh = serializers.CharField()


class UserLogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(
        write_only=True, trim_whitespace=False)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        validate_password(value, user=self.context['request'].user)
        return value

    def validate(self, attrs):
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from current password."}
            )
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
