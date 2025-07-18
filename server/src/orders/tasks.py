from celery import shared_task

from django.utils import timezone
from datetime import timedelta

from src.orders.models import Order
from src.orders.choices import OrderStatusChoices

@shared_task
def complete_old_orders():
    cutoff = timezone.now() - timedelta(days=2)
    # cutoff = timezone.now() - timedelta(seconds=30) # For testing
    Order.objects.filter(
        status=OrderStatusChoices.PENDING, 
        created_at__lt=cutoff
        ).update(
            status=OrderStatusChoices.COMPLETED
            )
