from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from src.accounts.models.user_photo import UserPhoto
from src.accounts.models.user_profile import UserProfile


UserModel = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_user_models(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserPhoto.objects.get_or_create(user=instance)
