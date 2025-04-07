import os
import django
from django.core.management.base import (
    BaseCommand,
)
from django.contrib.contenttypes.models import ContentType

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

        gemstone_choices = dict(Product.GEMSTONE_CHOICES)
        pink_sapphire = list(gemstone_choices.keys())[0]
        blue_sapphire = list(gemstone_choices.keys())[1]
        brilliant_diamond = list(gemstone_choices.keys())[2]

        gemstone_types = [pink_sapphire, blue_sapphire, brilliant_diamond]

        for product in products_by_size_and_price:
            
            classToInstantiate = product['class']
            class_name = classToInstantiate.__name__
            sizes = product['sizes']
            prices = product['prices']
            default_quantity = 2

            for gemstone_type in gemstone_types:

                for size_index in range(len(sizes)):

                    size = sizes[size_index]
                    price = prices[size_index]
                    first_image_url = products_by_images_and_description[
                        class_name][gemstone_type]['first_image_url']
                    second_image_url = products_by_images_and_description[
                        class_name][gemstone_type]['second_image_url']
                    description = products_by_images_and_description[
                        class_name][gemstone_type]['description'],

                    product = classToInstantiate(
                        gemstone=gemstone_type,
                        first_image_url=first_image_url,
                        second_image_url=second_image_url,
                        description=description,
                    )

                    product.save()

                    Inventory.objects.create(
                        content_type=ContentType.objects.get_for_model(
                            classToInstantiate),
                        object_id=product.id,
                        price=price,
                        quantity=default_quantity,
                        size=size,
                    )

        # necklace_xs = 38.53
        # necklace_s = 40.64
        # necklace_m = 43.18
        # necklace_l = 45.72
        # necklace_xl = 47.46

        # pendant_xs = 39.53,
        # pendant_s = 41.64,
        # pendant_m = 44.18,
        # pendant_l = 46.72,
        # pendant_xl = 48.46,

        # bracelet_xs = 13.1,
        # bracelet_s = 15.2,
        # bracelet_m = 17.8,
        # bracelet_l = 19.3,
        # bracelet_xl = 20.2,

        # ring_xs = 3.04,
        # ring_s = 4.05,
        # ring_m = 4.98,
        # ring_l = 5.86,
        # ring_xl = 6.34,

        # charm_size = 1.6

        # drop_earring_size = 4.6

        # stood_earring_size = 0.51

        # pink_drop_earring_xs = DropEarring(
        #     gemstone=pink_sapphire,
        #     first_image_url='https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-1_zzaw4q_yqmref.webp',
        #     second_image_url='https://res.cloudinary.com/dpgvbozrb/image/upload/v1743957283/forget_me_not_drop_earrings_diamond_and_pink_sapphire_eapspdrflrfmn_ee-1_zzaw4q_yqmref.webp',
        #     description='desc',
        # )

        # pink_drop_earring_xs.save()

        # Inventory.objects.create(
        #     content_type=ContentType.objects.get_for_model(DropEarring),
        #     object_id=pink_drop_earring_xs.id,
        #     price=1000,
        #     quantity=2,
        #     size=drop_earring_size,
        # )

    #     blue_necklace = Necklace(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_necklace.save()

    #     white_ring = Ring(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_ring.save()

    #     pink_bracelet = Bracelet(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_bracelet.save()

    #     blue_stud_earring = StudEarring(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_stud_earring.save()

    #     white_pendant = Pendant(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_pendant.save()

    #     pink_charm = Charm(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_charm.save()

    # ###

    #     blue_drop_earring = DropEarring(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_drop_earring.save()

    #     white_necklace = Necklace(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_necklace.save()

    #     pink_ring = Ring(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_ring.save()

    #     blue_bracelet = Bracelet(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_bracelet.save()

    #     white_stud_earring = StudEarring(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_stud_earring.save()

    #     pink_pendant = Pendant(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_pendant.save()

    #     blue_charm = Charm(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_charm.save()

    #     ###

    #     white_drop_earring = DropEarring(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_drop_earring.save()

    #     pink_necklace = Necklace(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_necklace.save()

    #     blue_ring = Ring(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_ring.save()

    #     white_bracelet = Bracelet(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_bracelet.save()

    #     pink_stud_earring = StudEarring(
    #         gemstone=pink_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     pink_stud_earring.save()

    #     blue_pendant = Pendant(
    #         gemstone=blue_sapphire,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     blue_pendant.save()

    #     white_charm = Charm(
    #         gemstone=brilliant_diamond,
    #         first_image_url='',
    #         second_image_url='',
    #         description='',
    #         price='',
    #         quantity=2,
    #         size='',
    #     )

    #     white_charm.save()
