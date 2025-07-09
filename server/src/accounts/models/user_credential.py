from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from src.accounts.managers import UserCredentialManager
from src.accounts.validators.models import UsernameValidator
from src.accounts.constants import UserFieldLengths, UserErrorMessages


class UserCredential(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': UserErrorMessages.EMAIL_UNIQUE,
        }
    )

    username = models.CharField(
        max_length=UserFieldLengths.USERNAME_MAX,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': UserErrorMessages.USERNAME_UNIQUE,
        }
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    agreed_to_emails = models.BooleanField(
        default=False,
    )

    objects = UserCredentialManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
