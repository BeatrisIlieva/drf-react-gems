from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from src.accounts.serializers import (
    UserLoginRequestSerializer,
    UserLoginResponseSerializer,
    UserLogoutRequestSerializer,
    UserRegisterSerializer,
)


UserModel = get_user_model()


class UserRegisterView(CreateAPIView):
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

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'id': user.pk,

            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=['Authentication'],
    summary='Login endpoint',
    description='Authenticate user and get back access and refresh tokens',
    request=UserLoginRequestSerializer,
    responses={
        200: UserLoginResponseSerializer,
        401: 'Invalid username or password'
    }
)
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # in DRF `request.data` is like `request.POST` and `request.GET` in Django
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {
                    'error': 'Invalid username or password',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # if the user credentials are valid we issue both `access token` and `refresh token`
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                # the refresh token has a property `access_token`
                'access': str(refresh.access_token),
                'message': 'Login successful',
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=['Authentication'],
    summary='Logout endpoint',
    description='Blacklist the refresh token',
    request=UserLogoutRequestSerializer,
    responses={
        200: UserLogoutRequestSerializer,
        401: 'Invalid or expired token'
    }
)
class UserLogoutView(APIView):
    # upon logout we need to blacklist the token so it can be no longer used
    def post(self, request, *args, **kwargs):
        print(request.data)
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
