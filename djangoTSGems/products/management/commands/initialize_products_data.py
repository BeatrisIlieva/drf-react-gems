import os
import django
from django.core.management.base import (
    BaseCommand,
)

from djangoTSGems.products.management.products_data import products_by_size_and_price, products_by_images_and_description

from djangoTSGems.products.models import Product
from djangoTSGems.inventories.models import Inventory


class Command(BaseCommand):
    help = "Initialize data for your Django app"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_gems.settings")
        django.setup()

        self.stdout.write(self.style.SUCCESS(
            "Starting data initialization..."))

        self.create_products()

        self.stdout.write(
            self.style.SUCCESS("Data initialization completed successfully.")
        )

    def create_products(self):

        gemstone_types = ['PS', 'BS', 'BD']

        gemstone_index = 0

        for _ in range(3):

            for product in products_by_size_and_price:

                if gemstone_index == len(gemstone_types):
                    gemstone_index = 0

                category = product['category']
                sizes = product['sizes']
                prices = product['prices']
                default_quantity = 2

                gemstone_type = gemstone_types[gemstone_index]

                first_image_url = products_by_images_and_description[
                    category][gemstone_type]['first_image_url']
                second_image_url = products_by_images_and_description[
                    category][gemstone_type]['second_image_url']
                description = products_by_images_and_description[
                    category][gemstone_type]['description'],

                product = Product(
                    gemstone=gemstone_type,
                    first_image_url=first_image_url,
                    second_image_url=second_image_url,
                    description=description,
                )

                product.save()

                for size_index in range(len(sizes)):

                    size = sizes[size_index]
                    price = prices[size_index]
                    

                    Inventory.objects.create(
                        product=product,
                        price=price,
                        quantity=default_quantity,
                        size=size,
                    )

                gemstone_index += 1
