from celery import shared_task

from django.core.mail import send_mail


@shared_task
def _send_email(subject, message, html_message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
