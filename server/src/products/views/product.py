"""
This module contains views for product listing, detail, attribute retrieval, and review management.

It provides:
- List and detail views for each product type (Earwear, Neckwear, Wristwear, Fingerwear)
- Attribute views for product properties like color, metal, stone, and collection
- Both synchronous and asynchronous endpoints for attribute retrieval
- Custom permission for reviewer access to all product reviews
- Review management endpoints for products
"""

from typing import Type
from src.products.models.product import (
    Color,
    Metal,
    Stone,
    Collection
)
from src.products.serializers.product import (
    CollectionSerializer,
    ColorSerializer,
    EarwearItemSerializer,
    FingerwearItemSerializer,
    MetalSerializer,
    NeckwearItemSerializer,
    NeckwearListSerializer,
    EarwearListSerializer,
    StoneSerializer,
    WristwearItemSerializer,
    WristwearListSerializer,
    FingerwearListSerializer
)
from src.products.models import (
    Earwear,
    Neckwear,
    Wristwear,
    Fingerwear
)
from src.products.views.base import (
    BaseAttributeView,
    BaseProductItemView,
    BaseProductListView,
    AsyncBaseAttributeView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.permissions import BasePermission


class EarwearListView(BaseProductListView):
    model: Type[Earwear] = Earwear
    serializer_class = EarwearListSerializer


class NeckwearListView(BaseProductListView):
    model: Type[Neckwear] = Neckwear
    serializer_class = NeckwearListSerializer


class WristwearListView(BaseProductListView):
    model: Type[Wristwear] = Wristwear
    serializer_class = WristwearListSerializer


class FingerwearListView(BaseProductListView):
    model: Type[Fingerwear] = Fingerwear
    serializer_class = FingerwearListSerializer


class EarwearItemView(BaseProductItemView):
    model: Type[Earwear] = Earwear
    serializer_class = EarwearItemSerializer


class NeckwearItemView(BaseProductItemView):
    model: Type[Neckwear] = Neckwear
    serializer_class = NeckwearItemSerializer


class WristwearItemView(BaseProductItemView):
    model: Type[Wristwear] = Wristwear
    serializer_class = WristwearItemSerializer


class FingerwearItemView(BaseProductItemView):
    model: Type[Fingerwear] = Fingerwear
    serializer_class = FingerwearItemSerializer


class CollectionRetrieveView(BaseAttributeView):
    model: Type[Collection] = Collection
    serializer_class = CollectionSerializer


class ColorRetrieveView(BaseAttributeView):
    model: Type[Color] = Color
    serializer_class = ColorSerializer


class MetalRetrieveView(BaseAttributeView):
    model: Type[Metal] = Metal
    serializer_class = MetalSerializer


class StoneRetrieveView(BaseAttributeView):
    model: Type[Stone] = Stone
    serializer_class = StoneSerializer


class AsyncCollectionRetrieveView(AsyncBaseAttributeView):
    model: Type[Collection] = Collection
    serializer_class = CollectionSerializer


class AsyncColorRetrieveView(AsyncBaseAttributeView):
    model: Type[Color] = Color
    serializer_class = ColorSerializer


class AsyncMetalRetrieveView(AsyncBaseAttributeView):
    model: Type[Metal] = Metal
    serializer_class = MetalSerializer


class AsyncStoneRetrieveView(AsyncBaseAttributeView):
    model: Type[Stone] = Stone
    serializer_class = StoneSerializer


class IsReviewer(BasePermission):
    """
    Allows access only to users with the products.approve_review permission.
    """

    def has_permission(self, request, view):
        return request.user and request.user.has_perm('products.approve_review')


class ProductAllReviewsView(APIView):
    permission_classes = [IsAuthenticated, IsReviewer]

    def get(self, request, category, pk):
        # Map category to model
        from src.products.models.product import Earwear, Neckwear, Fingerwear, Wristwear
        model_map = {
            'earwear': Earwear,
            'neckwear': Neckwear,
            'fingerwear': Fingerwear,
            'wristwear': Wristwear,
        }
        model = model_map.get(category.lower())
        if not model:
            return Response({'detail': 'Invalid category.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Get all reviews for this product
        content_type = ContentType.objects.get_for_model(model)
        reviews = Review.objects.filter(
            content_type=content_type, object_id=product.id).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'reviews': serializer.data})
