import os
import random
import django
from django.core.management.base import BaseCommand

from src.products.management.commands.utils.create_product import (
    create_product,
)
from src.products.management.products_data import products_data
from src.products.management.commands.utils.attributes_as_list_mapper import (
    attributes_as_list_mapper,
)


class Command(BaseCommand):
    help = 'Creating products'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

        django.setup()

        self.stdout.write(self.style.SUCCESS('Starting creating products...'))

        self.initialize_data()

        self.stdout.write(
            self.style.SUCCESS('All products created successfully.')
        )

    def initialize_data(self):

        for model, list in attributes_as_list_mapper.items():
            for element in list:
                model.objects.create(
                    name=element,
                )

        random.shuffle(products_data)

        for product_data in products_data:
            create_product(product_data)
