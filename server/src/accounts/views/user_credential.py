from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
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
    # uses signal to create related models
    # like `UserProfile`, `UserAddress`, `UserPhoto`
    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer
    # because in `settings.py` we defined that by default
    # we expect the user to be authenticated
    # we need to add `AllowAny` permission for the `UserRegisterView`
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Use the original serializer to validate and save the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens for the newly created user
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

    def post(self, request, *args, **kwargs):
        # Validate the request data using the serializer
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract validated data
        email_or_username = serializer.validated_data['email_or_username']
        password = serializer.validated_data['password']

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

        # if the user credentials are valid we issue both `access token` and `refresh token`
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                # the refresh token has a property `access_token`
                'access': str(refresh.access_token),
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'id': user.pk,
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    # upon logout we need to blacklist the token so it can be no longer used
    def post(self, request, *args, **kwargs):
        try:
            # we get the token from the request as a string
            refresh_token = request.data.get('refresh')
            # we create a token object
            token = RefreshToken(refresh_token)
            # in order to call its method `blacklist` which adds the token
            # into the table containing the blacklisted tokens
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

    def patch(self, request):
        """
        Change user password
        """
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

    def get_object(self):
        return self.request.user
