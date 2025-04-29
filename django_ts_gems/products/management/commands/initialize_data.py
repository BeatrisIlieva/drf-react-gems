import os
import django
from django.core.management.base import BaseCommand

from django_ts_gems.products.management.commands.utils.create_inventory import create_inventory
from django_ts_gems.products.management.commands.utils.create_product import create_product
from django_ts_gems.products.management.commands.utils.create_choices import create_choices
from django_ts_gems.products.management.data import products_data


class Command(BaseCommand):
    help = "Initialize data for your Django app"

    def handle(self, *args, **options):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "django_ts_gems.settings"
        )

        django.setup()

        self.stdout.write(self.style.SUCCESS(
            "Starting data initialization..."
        ))

        self.initialize_data()

        self.stdout.write(
            self.style.SUCCESS(
                "Data initialization completed successfully."
            )
        )

    def initialize_data(self):

        create_choices()

        for product_data in products_data:
            product = create_product(product_data)
            price = product_data['price']

            create_inventory(product, price)
