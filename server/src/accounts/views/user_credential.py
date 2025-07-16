"""
This module defines API views for user registration, login, logout, password change, and account deletion.

Key features:
- User registration with email and password
- User login with email or username
- JWT token issuance and blacklisting
- Password change for authenticated users
- Account deletion for authenticated users
- Guest data migration on registration/login
"""

from typing import Any
from django.contrib.auth import get_user_model, authenticate

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from src.accounts.serializers.user_credential import (
    UserRegisterSerializer,
    UserLoginRequestSerializer,
    PasswordChangeSerializer,
)
from src.accounts.constants import UserErrorMessages
from src.accounts.utils import migrate_guest_data_to_user

UserModel = get_user_model()


class UserRegisterView(CreateAPIView):
    """
    Uses a signal to create related UserProfile and UserPhoto models.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        # Validate incoming registration data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the new user instance
        user = serializer.save()

        # Issue JWT refresh and access tokens for the new user
        refresh = RefreshToken.for_user(user)

        # Migrate any guest data (e.g., shopping cart) to the new user
        guest_id = request.headers.get('Guest-Id')
        migrate_guest_data_to_user(user, guest_id)

        # Return tokens and user info to the frontend
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'username': user.username,
                'id': user.pk,
            },
            status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    """
    - Accepts email or username and password.
    - Authenticates the user and issues JWT tokens.
    - Migrates guest data if present.
    - Allows any user to attempt login.
    """
    permission_classes = [AllowAny]

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        # Validate login credentials
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract validated credentials
        email_or_username: str = serializer.validated_data['email_or_username']
        password: str = serializer.validated_data['password']

        # Authenticate user (returns user instance or None)
        user = authenticate(
            username=email_or_username,
            password=password,
        )

        if user is None:
            # Invalid credentials
            return Response(
                {'error': UserErrorMessages.INCORRECT_CREDENTIALS},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Migrate guest data if present
        guest_id = request.headers.get('Guest-Id')
        migrate_guest_data_to_user(user, guest_id)

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

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        try:
            # Get refresh token from request data
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            # Blacklist the token (requires blacklist app enabled)
            token.blacklist()

            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK,
            )

        except TokenError:
            # Token is invalid or already expired/blacklisted
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordChangeView(APIView):
    """
    - Only accessible to authenticated users.
    - Validates current and new passwords.
    - Saves the new password if validation passes.
    """
    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request: Request
    ) -> Response:
        # Validate current and new passwords
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(DestroyAPIView):
    """
    - Only accessible to authenticated users.
    - Deletes the user instance associated with the current request.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Any:
        # Return the current user instance for deletion
        return self.request.user
