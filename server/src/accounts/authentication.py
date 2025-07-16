"""
CustomAuthBackendBackend:
- Allows authentication with email OR username
"""

from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest

UserModel = get_user_model()


class CustomAuthBackendBackend(ModelBackend):
    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[Any]:
        try:
            # Try to find a user with the provided username/email
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            # This indicates authentication failure
            return None

        # check_password() compares the provided password with the stored hash
        # user_can_authenticate() checks if the user is active and not blocked
        if user.check_password(password) and self.user_can_authenticate(user):
            # Return the authenticated user object
            return user

        # Return None if password is incorrect or user cannot authenticate
        return None
