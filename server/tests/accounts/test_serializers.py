from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

from rest_framework.test import APITestCase
from src.accounts.serializers.user_credential import (
    PasswordResetConfirmSerializer,
    UserPasswordResetRequestSerializer,
)


UserModel = get_user_model()


class PasswordResetSerializerTests(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@mail.com',
            username='test',
            password='!1Aabb',
            is_active=True,
        )

    def test_password_reset_request_serializer_valid(self):
        serializer = UserPasswordResetRequestSerializer(
            data={'email': 'test@mail.com'}
        )
        self.assertTrue(serializer.is_valid())

    def test_password_reset_confirm_serializer_valid(self):

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        data = {'uid': uid, 'token': token, 'new_password': '!1Aabbb'}

        serializer = PasswordResetConfirmSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('!1Aabbb'))
