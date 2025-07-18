from celery import shared_task
from django.db.models import F

from django.utils import timezone
from datetime import timedelta

from src.products.models.inventory import Inventory
from src.shopping_bags.models import ShoppingBag


@shared_task
def cleanup_expired_bags():
    cutoff_date = timezone.now() - timedelta(days=2)
    # cutoff_date = timezone.now() - timedelta(seconds=15) # For testing

    expired_bags = ShoppingBag.objects.filter(
        user__isnull=True,
        created_at__lt=cutoff_date,
    )

    for bag in expired_bags:
        inventory_id = bag.inventory_id
        quantity = bag.quantity
        Inventory.objects.filter(id=inventory_id).update(
            quantity=F('quantity') + quantity)

        bag.delete()
