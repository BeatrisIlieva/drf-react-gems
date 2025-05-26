import os
import random
from random import choice, randint
import django
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
from faker import Faker

from src.products.models.fingerwear import Fingerwear
from src.products.models.review import Review


UserModel = get_user_model()

fake = Faker()

sample_reviews = [
    "Beautiful piece, exactly as described. The craftsmanship is impressive, and it really stands out when I wear it to special occasions.",
    "Sturdy and well-crafted, I get compliments all the time. It feels durable and looks elegant, definitely worth the price I paid.",
    "The gemstone sparkles brilliantly in the light, catching everyone's attention. It adds just the right amount of sparkle to any outfit.",
    "Very comfortable to wear even all day long. I barely notice it’s there, and it doesn’t irritate my skin at all.",
    "A bit smaller than I expected, but still lovely. It’s delicate and subtle, which suits my style perfectly.",
    "Shipping was fast and the packaging was excellent. The item arrived safely and looked brand new right out of the box.",
    "Perfect gift for my partner, highly recommend! They absolutely loved it and wear it every day without fail.",
    "Exceeded my expectations in every way! The design is unique and the quality feels premium. I’ve already gotten several compliments.",
    "Lovely piece with a timeless style. It matches both casual and formal outfits effortlessly. Definitely a staple in my collection now.",
    "The attention to detail is remarkable. You can tell a lot of care went into making this piece. I’m really happy with my purchase.",
    "The clasp is sturdy and secure, which is important to me. I wear it daily without worrying about it falling off or breaking.",
    "Received many compliments and inquiries about where I got it. It’s become a conversation starter wherever I go!",
    "The stones are well set and the finish is flawless. It looks expensive but was surprisingly affordable.",
    "I appreciate how lightweight this piece is. It doesn’t feel bulky or heavy like some jewelry can, making it comfortable all day long.",
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
            {'email': 'simon.smith@mail.com', 'password': '!1Aabb', 'first_name': 'Simon',
                'last_name': 'Smith', 'photo': 'image/upload/v1748258755/boy2_aijwxt_rqfolu.jpg'},

            {'email': 'emma.watson@mail.com', 'password': '!1Aabb', 'first_name': 'Emma',
                'last_name': 'Watson', 'photo': 'image/upload/v1748258754/girl2_rjcjz2_y54zla.jpg'},
            {'email': 'olivia.smith@mail.com', 'password': '!1Aabb', 'first_name': 'Olivia', 'last_name': 'Smith',
             'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-bokeh-background_wyylpf_seqqgg.jpg'},
            {'email': 'ava.johnson@mail.com', 'password': '!1Aabb', 'first_name': 'Ava', 'last_name': 'Johnson',
             'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-with-backpack-her-hands_fxkmfo_nflhb4.jpg'},
            {'email': 'sophia.brown@mail.com', 'password': '!1Aabb', 'first_name': 'Sophia', 'last_name': 'Brown',
             'photo': 'image/upload/v1748258753/3d-illustration-cute-little-girl-hat-jacket_bdlvpk_qo4b95.jpg'},
            {'email': 'isabella.jones@mail.com', 'password': '!1Aabb', 'first_name': 'Isabella',
             'last_name': 'Jones', 'photo': 'image/upload/v1748258753/girl1_lclcth_lqhndu.jpg'},

            {'email': 'michael.clark@mail.com', 'password': '!1Aabb', 'first_name': 'Michael', 'last_name': 'Clark',
             'photo': 'image/upload/v1748258754/little-boy-cap-with-backpack-street-3d-rendering_i2mw52_frkquw.jpg'},
            {'email': 'william.lewis@mail.com', 'password': '!1Aabb', 'first_name': 'William',
             'last_name': 'Lewis', 'photo': 'image/upload/v1748258753/boy1_cli59g_czbmce.jpg'}
        ]

        created_users = []

        for item in users_data:
            user = UserModel.objects.create(email=item['email'])
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
        fingerwear_content_type = ContentType.objects.get_for_model(Fingerwear)

        for product in fingerwears:
            shuffled_users = users.copy()
            random.shuffle(shuffled_users)

            for user in shuffled_users[:3]:
                rating = randint(2, 5)
                comment = random.choice(sample_reviews)

                Review.objects.create(
                    user=user,
                    rating=rating,
                    comment=comment,
                    content_type=fingerwear_content_type,
                    object_id=product.pk,
                )
