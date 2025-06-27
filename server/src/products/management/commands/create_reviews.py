import os
import random
from random import randint
import django
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
from faker import Faker

from src.products.models import (
    Earwear,
    Fingerwear,
    Neckwear,
    Review,
    Wristwear
)


UserModel = get_user_model()

fake = Faker()

sample_reviews = [
    "Beautiful piece, exactly as described. The craftsmanship is impressive, and it really stands out on special occasions.",
    "The gemstone sparkles brilliantly in the light, catching everyone's attention. It adds just the right amount of sparkle to any outfit.",
    "A bit smaller than expected, but still lovely. It’s delicate and subtle, fitting perfectly with many styles.",
    "Shipping was fast and the packaging was excellent. The item arrived safely and looked brand new right out of the box.",
    "Perfect gift for a loved one, highly recommend! They wear it every day without fail.",
    "The attention to detail is remarkable. You can tell a lot of care went into making this piece. I’m very happy with my purchase.",
    "The stones are well set and the finish is flawless. It looks expensive but was surprisingly affordable.",
    "I bought this as a gift, and it was very well received. The recipient hasn’t taken it off since!",
    "Comfortable, stylish, and well-made — everything I was looking for in a jewelry piece.",
    "This item exceeded my expectations for the price. It’s now a favorite in my collection.",
    "It looks great with both casual clothes and more formal attire, very versatile.",
    "I appreciate the durability — it’s been through daily wear and still looks new.",
    "The packaging was lovely, making it perfect for gifting right away.",
    "Subtle yet elegant — just the right touch without being too flashy. Works with all kinds of looks.",
    "Feels personal and thoughtfully made. It really shows that it’s crafted with intention.",
    "This piece has a timeless design that fits any style, whether minimal or bold.",
    "Matches beautifully with other accessories, and the quality is consistent across the board.",
    "It arrived ready to gift, with care in every detail — from the item itself to the packaging."
]


class Command(BaseCommand):
    help = 'Creating products'

    def handle(self, *args, **options):
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE',
            'src.settings'
        )

        django.setup()

        self.stdout.write(self.style.SUCCESS(
            'Starting creating reviews...'
        ))

        created_users = self.create_fake_users()
        self.create_fake_reviews(created_users)

        self.stdout.write(
            self.style.SUCCESS(
                'All reviews created successfully.'
            )
        )

    def create_fake_users(self):

        users_data = [
            {
                'username': 'Simon',
                'email': 'simon.smith@mail.com',
                'password': '!1Aabb',
                'first_name': 'Simon',
                'last_name': 'Smith',
                'photo': 'image/upload/v1748258755/boy2_aijwxt_rqfolu.jpg'
            },
            {
                'username': 'Ava',
                'email': 'ava.johnson@mail.com',
                'password': '!1Aabb',
                'first_name': 'Ava',
                'last_name': 'Johnson',
                'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-with-backpack-her-hands_fxkmfo_nflhb4.jpg'
            },
            {
                'username': 'Sophia',
                'email': 'sophia.brown@mail.com',
                'password': '!1Aabb',
                'first_name': 'Sophia',
                'last_name': 'Brown',
                'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-hat-jacket_bdlvpk_qo4b95.jpg'
            },
            {
                'username': 'Michael',
                'email': 'michael.clark@mail.com',
                'password': '!1Aabb',
                'first_name': 'Michael',
                'last_name': 'Clark',
                'photo': 'image/upload/v1748258754/little-boy-cap-with-backpack-street-3d-rendering_i2mw52_frkquw.jpg'
            },
            {
                'username': 'Emma',
                'email': 'emma.watson@mail.com',
                'password': '!1Aabb',
                'first_name': 'Emma',
                'last_name': 'Watson',
                'photo': 'image/upload/v1748258754/girl2_rjcjz2_y54zla.jpg'
            },
            {
                'username': 'Olivia',
                'email': 'olivia.smith@mail.com',
                'password': '!1Aabb',
                'first_name': 'Olivia',
                'last_name': 'Smith',
                'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-bokeh-background_wyylpf_seqqgg.jpg'
            },
            {
                'username': 'William',
                'email': 'william.lewis@mail.com',
                'password': '!1Aabb',
                'first_name': 'William',
                'last_name': 'Lewis',
                'photo': 'image/upload/v1748258753/boy1_cli59g_czbmce.jpg'
            },
            {
                'username': 'Isabella',
                'email': 'isabella.jones@mail.com',
                'password': '!1Aabb',
                'first_name': 'Isabella',
                'last_name': 'Jones',
                'photo': 'image/upload/v1748258753/girl1_lclcth_lqhndu.jpg'
            },

            {
                'username': 'Mia',
                'email': 'mia.davis@mail.com',
                'password': '!1Aabb',
                'first_name': 'Mia',
                'last_name': 'Davis',
                'photo': 'image/upload/v1748267948/bambino-cartoon-carino-che-posa-per-il-ritratto_z6edpw.jpg',
            },
            {
                'username': 'Liam',
                'email': 'liam.martin@mail.com',
                'password': '!1Aabb',
                'first_name': 'Liam',
                'last_name': 'Martin',
                'photo': 'image/upload/v1748267949/l-uomo-del-fitness-dei-cartoni-animati-3d_egayjv.jpg',
            },
            {
                'username': 'Amelia',
                'email': 'amelia.wilson@mail.com',
                'password': '!1Aabb',
                'first_name': 'Amelia',
                'last_name': 'Wilson',
                'photo': 'image/upload/v1748267948/cute-cartoon-kid-posing-portrait_kknsfr.jpg',
            },
        ]

        created_users = []

        for item in users_data:
            user, created = UserModel.objects.get_or_create(
                email=item['email'],
                defaults={
                    'username': item['username']
                }
            )
            
            if created:
                user.set_password(item['password'])
                user.save()

                user.userprofile.first_name = item['first_name']
                user.userprofile.last_name = item['last_name']
                user.userprofile.save()

                user.userphoto.photo = item['photo']
                user.userphoto.save()

            created_users.append(user)

        return created_users

    def create_fake_reviews(self, users):
        fingerwears = Fingerwear.objects.all()
        wristwears = Wristwear.objects.all()
        neckwears = Neckwear.objects.all()
        earwears = Earwear.objects.all()

        fingerwear_content_type = ContentType.objects.get_for_model(Fingerwear)
        wristwears_content_type = ContentType.objects.get_for_model(Wristwear)
        neckwears_content_type = ContentType.objects.get_for_model(Neckwear)
        earwears_content_type = ContentType.objects.get_for_model(Earwear)

        all_products_with_their_content_types = [
            [fingerwears, fingerwear_content_type],
            [wristwears, wristwears_content_type],
            [neckwears, neckwears_content_type],
            [earwears, earwears_content_type],
        ]

        for element in all_products_with_their_content_types:
            products, content_type = element

            for product in products:

                shuffled_users = users.copy()
                random.shuffle(shuffled_users)

                for user in shuffled_users:
                    rating = randint(3, 5)
                    comment = random.choice(sample_reviews)

                    Review.objects.create(
                        user=user,
                        rating=rating,
                        approved=True,
                        comment=comment,
                        content_type=content_type,
                        object_id=product.pk,
                    )
