from src import settings

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from src.common.views import _send_email
from src.accounts.models.user_photo import UserPhoto
from src.accounts.models.user_profile import UserProfile


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_related_user_models(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserPhoto.objects.get_or_create(user=instance)

        html_message = render_to_string(
            'mailer/registration-greeting.html', {'user': instance}
        )
        plain_message = strip_tags(html_message)

        _send_email.delay(
            subject='Welcome to DRF React Gems!',
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(instance.email,),
        )
