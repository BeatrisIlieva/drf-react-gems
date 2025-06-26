from django.contrib.auth import get_user_model
from django.db import models

from cloudinary.models import CloudinaryField

UserModel = get_user_model()


class UserPhoto(models.Model):
    photo = CloudinaryField(
        'image',
        null=True,
        blank=False,
        default='image/upload/v1750959197/user-1699635_1280_z3dgxn.png'
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
