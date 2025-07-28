from datetime import timedelta
from django.utils import timezone
from django.test import TestCase

from tests.common.test_data_builder import TestDataBuilder
from src.orders.tasks import complete_old_orders
from src.orders.choices import OrderStatusChoices
from src.orders.models import Order


class CompleteOldOrdersTaskTest(TestCase):

    def setUp(self):
        """Set up test data before each test method."""
        self.now = timezone.now()

    def test_completes_old_pending_orders(self):
        """Test that orders older than 1 day with PENDING status are completed."""

        product_with_inventory = TestDataBuilder.create_product_with_inventory()
        user = TestDataBuilder.create_authenticated_user()

        old_order = Order.objects.create(
            inventory=product_with_inventory['inventory'],
            user=user,
            quantity=1,
        )

        Order.objects.filter(id=old_order.id).update(
            created_at=self.now - timedelta(days=2))
        old_order.refresh_from_db()

        complete_old_orders()

        old_order.refresh_from_db()

        self.assertEqual(old_order.status, OrderStatusChoices.COMPLETED)
