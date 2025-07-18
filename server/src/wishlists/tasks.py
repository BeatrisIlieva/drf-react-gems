from celery import shared_task

from django.utils import timezone
from datetime import timedelta

from src.wishlists.models import Wishlist


@shared_task
def cleanup_expired_wishlists():
    # cutoff_date = timezone.now() - timedelta(days=2)
    cutoff_date = timezone.now() - timedelta(seconds=15) # For testing, set to 30 seconds

    Wishlist.objects.filter(
        user__isnull=True,
        created_at__lt=cutoff_date,
    ).delete()

