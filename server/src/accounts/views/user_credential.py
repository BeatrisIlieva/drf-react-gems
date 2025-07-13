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

from src.accounts.utils import migrate_guest_data_to_user


UserModel = get_user_model()


class UserRegisterView(CreateAPIView):
    # uses signal to create related models `UserProfile` and `UserPhoto`
    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        guest_id = request.headers.get('Guest-Id')
        migrate_guest_data_to_user(user, guest_id)

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
    permission_classes = [AllowAny]

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_or_username: str = serializer.validated_data['email_or_username']
        password: str = serializer.validated_data['password']

        user = authenticate(
            username=email_or_username,
            password=password,
        )

        if user is None:
            return Response(
                {
                    'error': 'Invalid username or password',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        guest_id = request.headers.get('Guest-Id')
        migrate_guest_data_to_user(user, guest_id)

        refresh = RefreshToken.for_user(user)

        # Get user permissions for frontend role-based functionality
        permissions = []
        if user.has_perm('products.approve_review'):
            permissions.append('products.approve_review')

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
    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    'message': 'Logout successful',
                },
                status=status.HTTP_200_OK,
            )

        except TokenError:
            return Response(
                {
                    'error': 'Invalid or expired token',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request: Request
    ) -> Response:
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
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Any:
        return self.request.user
