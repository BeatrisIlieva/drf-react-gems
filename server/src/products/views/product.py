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


# =============================================================================
# ASYNC ATTRIBUTE VIEWS FOR FILTERS
# =============================================================================
# These async views provide improved performance for concurrent filter requests.
# They are designed to handle multiple simultaneous requests for filter attributes
# and can be used alongside the synchronous views or as replacements.

class AsyncCollectionRetrieveView(AsyncBaseAttributeView):
    """
    Asynchronous view for retrieving collection filter data.
    
    This view provides async support for collection filtering, allowing
    for better performance when multiple filter requests are made
    simultaneously. It's particularly useful when the frontend needs
    to fetch multiple filter attributes at once.
    
    Usage:
    - Endpoint: /api/products/collections/async/
    - Query params: category (optional)
    - Returns: Collection data with counts for filtering
    """
    model: Type[Collection] = Collection
    serializer_class = CollectionSerializer


class AsyncColorRetrieveView(AsyncBaseAttributeView):
    """
    Asynchronous view for retrieving color filter data.
    
    This view provides async support for color filtering, enabling
    concurrent requests for color attribute data. It's optimized
    for scenarios where multiple filter attributes are requested
    simultaneously.
    
    Usage:
    - Endpoint: /api/products/colors/async/
    - Query params: category (optional)
    - Returns: Color data with counts for filtering
    """
    model: Type[Color] = Color
    serializer_class = ColorSerializer


class AsyncMetalRetrieveView(AsyncBaseAttributeView):
    """
    Asynchronous view for retrieving metal filter data.
    
    This view provides async support for metal filtering, allowing
    for improved performance when multiple filter requests are
    processed concurrently. It's designed to handle high-traffic
    scenarios efficiently.
    
    Usage:
    - Endpoint: /api/products/metals/async/
    - Query params: category (optional)
    - Returns: Metal data with counts for filtering
    """
    model: Type[Metal] = Metal
    serializer_class = MetalSerializer


class AsyncStoneRetrieveView(AsyncBaseAttributeView):
    """
    Asynchronous view for retrieving stone filter data.
    
    This view provides async support for stone filtering, enabling
    concurrent processing of stone attribute requests. It's optimized
    for scenarios where multiple filter attributes need to be
    retrieved simultaneously.
    
    Usage:
    - Endpoint: /api/products/stones/async/
    - Query params: category (optional)
    - Returns: Stone data with counts for filtering
    """
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
        reviews = Review.objects.filter(content_type=content_type, object_id=product.id).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'reviews': serializer.data})
