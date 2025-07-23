from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from src.common.tasks import _send_email
from src.products.models.review import Review


@receiver(signal=post_save, sender=Review)
def send_approval_email_notification(sender, instance, created, **kwargs):
    if not created and instance.approved:
        # delay -> comes from the decorator `@shared_task`; the `delay` method informs Celery
        # to put the task into a Redis queue and execute it when there is an available worker
        html_message = render_to_string(
            'mailer/review-approved.html', {'user': instance.user.username})
        plain_message = strip_tags(html_message)

        _send_email.delay(
            subject='Your product review has been approved!',
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(instance.user.email,),
        )
