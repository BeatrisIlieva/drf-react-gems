from django.contrib.auth import get_user_model
from django.db import models

from cloudinary.models import CloudinaryField

UserModel = get_user_model()


class UserPhoto(models.Model):
    photo = CloudinaryField(
        'image',
        null=True,
        blank=False,
        default='image/upload/v1748361714/silver-membership-icon-default-avatar-profile-icon-membership-icon-social-media-user-image-illustration-vector_mky68d.jpg'
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
