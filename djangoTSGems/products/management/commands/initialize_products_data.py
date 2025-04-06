import os
import django
from django.core.management.base import (
    BaseCommand,
)

from design_patterns_crafted_django_e_commerce.product.models import (
    Category,
    Color,
    Product,
)


class Command(BaseCommand):
    help = "Initialize data for your Django app"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_gems.settings")
        django.setup()

        self.stdout.write(self.style.SUCCESS(
            "Starting data initialization..."))

        self.bulk_create_product()

        self.stdout.write(
            self.style.SUCCESS("Data initialization completed successfully.")
        )

    def bulk_create_product(self):
        categories = Category.objects.all()
        colors = Color.objects.all()

        Product.objects.bulk_create(
            [
                Product(
                    first_image_url="https://res.cloudinary.com/deztgvefu/image/upload/v1723714885/forget-me-not-collection/earrings/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-1_zzaw4q.webp",
                    second_image_url="https://res.cloudinary.com/deztgvefu/image/upload/v1723714886/forget-me-not-collection/earrings/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-2_p9jicb.webp",
                    category=categories[0],
                    color=colors[0],
                    description="28 pear-shaped and round brilliant sapphires weighing a total of approximately 3.20 carats and 28 marquise and round brilliant diamonds weighing a total of approximately 1.98 carats, set in platinum.",
                ),

            ]
        )
