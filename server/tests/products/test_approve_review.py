from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from src.products.models.product import Collection, Color, Earwear, Metal, Stone
from src.products.models.review import Review
from tests.common.test_data_builder import TestDataBuilder

UserModel = get_user_model()


class TestApproveReview(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = TestDataBuilder.create_authenticated_user(
            'testuser', 'testuser')
        self.user.set_password('testpass123')
        self.review_content_type = ContentType.objects.get_for_model(Review)
        self.permission, _ = Permission.objects.get_or_create(
            codename='approve_review',
            content_type=self.review_content_type,
        )

        self.user.user_permissions.add(self.permission)
        self.user.save()

        self.collection = Collection.objects.create(name='Test collection')
        self.color = Color.objects.create(name='Test color')
        self.metal = Metal.objects.create(name='Test metal')
        self.stone = Stone.objects.create(name='Test stone')

        self.earwear = Earwear.objects.create(
            first_image='https://shared.example.com/image1.jpg',
            second_image='https://shared.example.com/image2.jpg',
            collection=self.collection,
            color=self.color,
            metal=self.metal,
            stone=self.stone
        )

        self.earwear_content_type = ContentType.objects.get_for_model(Earwear)

        self.review = Review.objects.create(
            rating=5,
            comment='Some text',
            content_type=self.earwear_content_type,
            object_id=self.earwear.pk,
            user=self.user,
        )

    def test_approve_valid_review(self):
        self.client.force_authenticate(user=self.user)

        self.client.post(
            reverse('review-approve', kwargs={'pk': self.review.pk}),
        )

        self.review.refresh_from_db()
        self.assertTrue(self.review.approved)

    def test_approve_valid_review(self):
        self.user.user_permissions.remove(self.permission)

        self.client.force_authenticate(user=self.user)

        self.client.post(
            reverse('review-approve', kwargs={'pk': self.review.pk}),
        )

        self.review.refresh_from_db()
        self.assertFalse(self.review.approved)
