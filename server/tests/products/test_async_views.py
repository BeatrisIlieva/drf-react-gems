from django.test import RequestFactory
from rest_framework.test import APITestCase
from rest_framework import status


from src.products.models import Collection, Color, Metal, Stone
from src.products.views.product import (
    AsyncCollectionRetrieveView,
    AsyncColorRetrieveView,
    AsyncMetalRetrieveView,
    AsyncStoneRetrieveView
)


class AsyncAttributeViewsTestCase(APITestCase):

    def setUp(self):
        self.factory = RequestFactory()

        # Create test attributes
        self.collection = Collection.objects.create(name='Test Collection')
        self.color = Color.objects.create(name='Test Color')
        self.metal = Metal.objects.create(name='Test Metal')
        self.stone = Stone.objects.create(name='Test Stone')

    def test_async_collection_retrieve_view(self):
        # Create request
        request = self.factory.get('/api/products/collections/async/')

        # Create view instance
        view = AsyncCollectionRetrieveView.as_view()

        # Test view execution
        response = view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_async_color_retrieve_view(self):
        # Create request
        request = self.factory.get('/api/products/colors/async/')

        # Create view instance
        view = AsyncColorRetrieveView.as_view()

        # Test view execution
        response = view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_async_metal_retrieve_view(self):
        # Create request
        request = self.factory.get('/api/products/metals/async/')

        # Create view instance
        view = AsyncMetalRetrieveView.as_view()

        # Test view execution
        response = view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_async_stone_retrieve_view(self):
        # Create request
        request = self.factory.get('/api/products/stones/async/')

        # Create view instance
        view = AsyncStoneRetrieveView.as_view()

        # Test view execution
        response = view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_async_views_with_category_filter(self):
        # Test with earwear category (singular form)
        request = self.factory.get(
            '/api/products/collections/async/?category=earwear')

        view = AsyncCollectionRetrieveView.as_view()

        # Test view execution
        response = view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
