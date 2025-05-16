from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    # when we create a user, in the response the hash password is sent
    # to resolve the problem we set the password to be write-only
    # write-only ensures that the password will not be returned in the response
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = UserModel
        # the serializer expects to receive json file containing `email` and `password`
        fields = ['email', 'password']

    def validate_password(self, value):
        # This will raise a ValidationError if the password is too short, common, numeric, etc.
        validate_password(value)
        return value

    # the default `create` method does not hash the password
    # that's why we override the `create` method to call `create_user`
    # which hashes the password
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id',  'email']
