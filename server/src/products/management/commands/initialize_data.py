import os
import django
from django.core.management.base import BaseCommand

from src.products.management.commands.utils.create_product_variant import create_product_variant
from src.products.management.commands.utils.create_product_item import create_product_item
from src.products.management.commands.utils.create_choices import create_choices
from src.products.management.commands.utils.create_stones_colors import create_stones_colors
from src.products.management.products_data import products_data


class Command(BaseCommand):
    help = "Initialize data for your Django app"

    def handle(self, *args, **options):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "src.settings"
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

        create_stones_colors()

        for product_data in products_data:
            product = create_product_item(product_data)
            price = product_data['price']

            create_product_variant(product, price)
