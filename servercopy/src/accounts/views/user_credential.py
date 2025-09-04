"""
This module defines API views for user registration, login, logout, password change, password reset and account deletion.
"""

from django.contrib.auth import get_user_model, authenticate

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema

from src.accounts.serializers.user_credential import (
    UserPasswordResetConfirmSerializer,
    UserPasswordResetRequestSerializer,
    UserRegisterSerializer,
    UserLoginRequestSerializer,
    UserPasswordChangeSerializer,
)
from src.accounts.constants import UserErrorMessages, UserSuccessMessages

UserModel = get_user_model()


class UserRegisterView(CreateAPIView):
    """
    Uses a signal to create related UserProfile and UserPhoto models.
    """

    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Validate incoming registration data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new user instance
        user = serializer.save()

        # Issue JWT refresh and access tokens for the new user
        refresh = RefreshToken.for_user(user)

        # Return tokens and user info to the frontend

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'username': user.username,
                'id': user.pk,
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    """
    - Accepts email or username and password.
    - Authenticates the user and issues JWT tokens.
    - Allows any user to attempt login.
    """

    permission_classes = [AllowAny]

    @extend_schema(request=UserLoginRequestSerializer)
    def post(self, request, *args, **kwargs):
        # Validate login credentials
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract validated credentials
        email_or_username = serializer.validated_data['email_or_username']
        password = serializer.validated_data['password']

        # Authenticate user (returns user instance or None)
        user = authenticate(
            username=email_or_username,
            password=password,
        )

        if user is None:
            # Invalid credentials
            return Response(
                {
                    'error': UserErrorMessages.INCORRECT_CREDENTIALS,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)

        # Collect user permissions for frontend role-based functionality
        permissions = []
        if user.has_perm('products.approve_review'):
            permissions.append('products.approve_review')

        # Return tokens, user info, and permissions

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'id': user.pk,
                'permissions': permissions,
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    """
    - Accepts a refresh token and blacklists it (invalidates the session).
    - Returns a success or error message.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Get refresh token from request data
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)

            # Blacklist the token (requires blacklist app enabled)
            token.blacklist()

            return Response(
                {
                    'message': UserSuccessMessages.LOGOUT_SUCCESS,
                },
                status=status.HTTP_200_OK,
            )

        except TokenError:
            # Token is invalid or already expired/blacklisted
            return Response(
                {
                    'error': UserErrorMessages.INVALID_TOKEN,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserPasswordChangeView(APIView):
    """
    - Only accessible to authenticated users.
    - Validates current and new passwords.
    - Saves the new password if validation passes.
    """
    @extend_schema(request=UserPasswordChangeSerializer)
    def patch(self, request):
        # Validate current and new passwords
        serializer = UserPasswordChangeSerializer(
            data=request.data,
            context={
                'request': request,
            },
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message': UserSuccessMessages.PASSWORD_CHANGED,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDeleteView(DestroyAPIView):
    """
    - Only accessible to authenticated users.
    - Deletes the user instance associated with the current request.
    """
    @extend_schema(
        summary='Delete user',
        description='Deletes the logged in user'
    )
    def get_object(self):
        # Return the current user instance for deletion

        return self.request.user


class UserPasswordResetRequestView(APIView):
    """Send password reset email"""

    permission_classes = [AllowAny]

    @extend_schema(request=UserPasswordResetRequestSerializer)
    def post(self, request):
        serializer = UserPasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message': UserSuccessMessages.RESET_LINK_SENT,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserPasswordResetConfirmView(APIView):
    """Reset password with token"""

    permission_classes = [AllowAny]

    @extend_schema(request=UserPasswordResetConfirmSerializer)
    def post(self, request):
        serializer = UserPasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message': UserSuccessMessages.PASSWORD_RESET,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
