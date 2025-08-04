"""
Views and async utilities for common backend operations, including:
- Sending reminder emails to users with uncompleted shopping bags
- Providing reviewer-only API to inspect old shopping bag items
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import asyncio

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from src.shopping_bags.models import ShoppingBag
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from src.common.tasks import _send_email
from src.common.permissions import IsOrderManager

UserModel = get_user_model()


async def send_email(
    subject, message, html_message, from_email, recipient_list
):
    """
    Asynchronously send an email using the configured email backend.
    Uses a Celery task to send the email in the background.
    """
    _send_email.delay(
        subject, message, html_message, from_email, recipient_list
    )


async def notify_users_they_have_uncompleted_orders(request):
    """
    Finds users with shopping bags older than one day and sends them a reminder email.
    - Queries ShoppingBag for bags created more than one day ago.
    - Sends an email to each user with such a bag.
    - Returns a JsonResponse with the list of user IDs notified.
    """
    one_day_ago = timezone.now() - timedelta(days=1)

    user_ids = await sync_to_async(
        lambda: list(
            ShoppingBag.objects.filter(
                created_at__lt=one_day_ago,
            )
            .values_list(
                'user',
                flat=True,
            )
            .distinct()
        )
    )()

    users = await sync_to_async(list)(
        UserModel.objects.filter(
            id__in=user_ids,
        )
    )

    html_message = render_to_string('mailer/uncompleted-orders.html')
    plain_message = strip_tags(html_message)

    email_tasks = [
        send_email(
            subject='Don’t Forget the Items in Your Shopping Bag!',
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(user.email,),
        )
        for user in users
    ]

    await asyncio.gather(*email_tasks)

    return JsonResponse({'detail': 'Emails have been sent'})


class ShoppingBagReminderInfoView(APIView):
    """
    API endpoint for reviewers to inspect shopping bags older than one day.
    - Only accessible to users with order manager permissions.
    - Returns a list of bag items with user and product info.
    """

    permission_classes = [IsOrderManager]

    @extend_schema(
        summary="Get shopping bag reminders",
        description="Returns shopping bags older than one day for order managers to review"
    )
    def get(self, request):
        one_day_ago = timezone.now() - timedelta(days=1)
        bag_items = ShoppingBag.objects.filter(
            created_at__lt=one_day_ago
        ).select_related(
            'user',
            'inventory',
        )

        data = [
            {
                'id': item.id,
                'created_at': item.created_at,
                'quantity': item.quantity,
                'total_price': (
                    item.inventory.price * item.quantity
                    if hasattr(item.inventory, 'price')
                    else None
                ),
                'user_email': item.user.email if item.user else None,
                'product_info': f'Size: {item.inventory.size} / Price: {item.inventory.price}',
            }
            for item in bag_items
        ]

        return Response(data)
