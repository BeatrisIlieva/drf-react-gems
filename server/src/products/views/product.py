"""
This module contains views for product listing, detail, attribute retrieval, and review management.

It provides:
- List and detail views for each product type (Earwear, Neckwear, Wristwear, Fingerwear)
- Attribute views for product properties like color, metal, stone, and collection
- Both synchronous and asynchronous endpoints for attribute retrieval
- Custom permission for reviewer access to all product reviews
- Review management endpoints for products
"""
import os
import tempfile

from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods


from src.common.permissions import IsOrderManager
from src.products.models.product import Color, Metal, Stone, Collection

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
    FingerwearListSerializer,
)

from src.products.models import Earwear, Neckwear, Wristwear, Fingerwear

from src.products.views.base import (
    BaseAttributeView,
    BaseProductItemView,
    BaseProductListView,
)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework import status


class EarwearListView(BaseProductListView):
    model = Earwear
    serializer_class = EarwearListSerializer


class NeckwearListView(BaseProductListView):
    model = Neckwear
    serializer_class = NeckwearListSerializer


class WristwearListView(BaseProductListView):
    model = Wristwear
    serializer_class = WristwearListSerializer


class FingerwearListView(BaseProductListView):
    model = Fingerwear
    serializer_class = FingerwearListSerializer


class EarwearItemView(BaseProductItemView):
    model = Earwear
    serializer_class = EarwearItemSerializer


class NeckwearItemView(BaseProductItemView):
    model = Neckwear
    serializer_class = NeckwearItemSerializer


class WristwearItemView(BaseProductItemView):
    model = Wristwear
    serializer_class = WristwearItemSerializer


class FingerwearItemView(BaseProductItemView):
    model = Fingerwear
    serializer_class = FingerwearItemSerializer


class CollectionRetrieveView(BaseAttributeView):
    model = Collection
    serializer_class = CollectionSerializer


class ColorRetrieveView(BaseAttributeView):
    model = Color
    serializer_class = ColorSerializer


class MetalRetrieveView(BaseAttributeView):
    model = Metal
    serializer_class = MetalSerializer


class StoneRetrieveView(BaseAttributeView):
    model = Stone
    serializer_class = StoneSerializer


class ProductAllReviewsView(APIView):
    permission_classes = [IsAuthenticated, IsOrderManager]

    def get(self, request, category, pk):

        model_map = {
            'earwear': Earwear,
            'neckwear': Neckwear,
            'fingerwear': Fingerwear,
            'wristwear': Wristwear,
        }

        model = model_map.get(category.lower())

        if not model:
            return Response(
                {'detail': 'Invalid category.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response(
                {'detail': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get all reviews for this product
        content_type = ContentType.objects.get_for_model(model)
        reviews = Review.objects.filter(
            content_type=content_type, object_id=product.id
        ).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)

        return Response({'reviews': serializer.data})


def catalog_page(request):
    """Display the catalog download page"""
    return render(request, 'catalog_download.html')


@require_http_methods(["POST"])
def generate_catalog(request):
    """Generate and return the PDF catalog"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        # Generate PDF
        call_command('generate_product_catalog', output=tmp_path)

        # Check if file was created successfully
        if not os.path.exists(tmp_path):
            return JsonResponse({'error': 'Failed to generate PDF'}, status=500)

        # Get file size
        file_size = os.path.getsize(tmp_path)

        # Read and return PDF
        with open(tmp_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        # Clean up temp file
        os.unlink(tmp_path)

        # Return PDF with proper headers
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product_catalog.pdf"'
        response['Content-Length'] = str(file_size)
        return response

    except Exception as e:
        return JsonResponse({'error': f'Error generating catalog: {str(e)}'}, status=500)


def download_catalog(request):
    """Legacy view - redirect to new page"""
    return catalog_page(request)
