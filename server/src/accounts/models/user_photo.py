"""
The UserPhoto model:
- Stores user profile pictures in the cloud via Cloudinary
- Uses one-to-one relationship with the user model
"""

from django.contrib.auth import get_user_model
from django.db import models

from cloudinary.models import CloudinaryField

from src.accounts.constants import PhotoSize
from src.accounts.validators.models import FileSizeValidator

UserModel = get_user_model()


class UserPhoto(models.Model):

    photo = CloudinaryField(
        'image',
        null=True,
        blank=False,
        validators=[
            FileSizeValidator(PhotoSize.MAX_SIZE),
        ],
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
