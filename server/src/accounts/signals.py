from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from src.accounts.models.user_photo import UserPhoto
from src.accounts.models.user_profile import UserProfile
from src.accounts.models.user_address import UserAddress


UserModel = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_address(sender, instance, created, **kwargs):
    if created:
        UserAddress.objects.create(
            user=instance,
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_photo(sender, instance, created, **kwargs):
    if created:
        UserPhoto.objects.create(
            user=instance,
        )
