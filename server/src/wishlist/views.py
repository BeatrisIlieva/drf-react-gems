from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
import uuid

from src.wishlist.models import Wishlist
from src.wishlist.serializers import WishlistSerializer, WishlistCreateSerializer, WishlistDeleteSerializer


class WishlistListView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['Wishlist'],
        summary='List wishlist items',
        description='Get all wishlist items for authenticated user or guest user via Guest-Id header',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Get wishlist items for authenticated user or guest"""
        if self.request.user.is_authenticated:
            return Wishlist.objects.filter(user=self.request.user)
        else:
            guest_id = self.request.headers.get('Guest-Id')
            if guest_id:
                try:
                    guest_id = uuid.UUID(guest_id)
                    return Wishlist.objects.filter(guest_id=guest_id, user__isnull=True)
                except ValueError:
                    return Wishlist.objects.none()
            return Wishlist.objects.none()


class WishlistCreateView(CreateAPIView):
    serializer_class = WishlistCreateSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['Wishlist'],
        summary='Add item to wishlist',
        description='Add a product to wishlist for authenticated user or guest user via Guest-Id header',
        request=WishlistCreateSerializer,
        responses={
            201: WishlistSerializer,
            400: 'Bad Request - Item already in wishlist or invalid data',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        content_type = serializer.validated_data['content_type']
        object_id = serializer.validated_data['object_id']
        
        # Get user and guest_id
        user = request.user if request.user.is_authenticated else None
        guest_id = request.headers.get('Guest-Id')
        
        # Validate guest_id format if provided
        if guest_id and not user:
            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response(
                    {'detail': 'Invalid guest ID format'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check if user is authenticated or has valid guest_id
        if not user and not guest_id:
            return Response(
                {'detail': 'User must be authenticated or provide valid Guest-Id header'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if item already exists in wishlist
        if user:
            existing_item = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=object_id
            ).first()
        else:
            existing_item = Wishlist.objects.filter(
                guest_id=guest_id,
                user__isnull=True,
                content_type=content_type,
                object_id=object_id
            ).first()
            
        if existing_item:
            return Response(
                {'detail': 'Item already in wishlist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create wishlist item
        if user:
            wishlist_item = Wishlist.objects.create(
                user=user,
                content_type=content_type,
                object_id=object_id
            )
        else:
            wishlist_item = Wishlist.objects.create(
                guest_id=guest_id,
                content_type=content_type,
                object_id=object_id
            )
        
        response_serializer = WishlistSerializer(wishlist_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class WishlistDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = WishlistDeleteSerializer  # For documentation purposes only
    
    @extend_schema(
        tags=['Wishlist'],
        summary='Remove item from wishlist',
        description='Remove a specific product from wishlist using content_type and object_id, Guest-Id header for non-authenticated users',
        responses={
            204: 'Item removed successfully',
            404: 'Item not found in wishlist',
        }
    )
    def delete(self, request, content_type, object_id, *args, **kwargs):
        # Get user and guest_id
        user = request.user if request.user.is_authenticated else None
        guest_id = request.headers.get('Guest-Id')
        
        # Validate guest_id format if provided
        if guest_id and not user:
            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response(
                    {'detail': 'Invalid guest ID format'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check if user is authenticated or has valid guest_id
        if not user and not guest_id:
            return Response(
                {'detail': 'User must be authenticated or provide valid Guest-Id header'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get content type object
        try:
            ct = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            return Response(
                {'detail': 'Invalid content type'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Find and delete wishlist item
        if user:
            wishlist_item = get_object_or_404(
                Wishlist,
                user=user,
                content_type=ct,
                object_id=object_id
            )
        else:
            wishlist_item = get_object_or_404(
                Wishlist,
                guest_id=guest_id,
                user__isnull=True,
                content_type=ct,
                object_id=object_id
            )
        
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistCountView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['Wishlist'],
        summary='Get wishlist count',
        description='Get the number of items in wishlist for authenticated user or guest user via Guest-Id header',
        responses={
            200: {'type': 'object', 'properties': {'count': {'type': 'integer'}}},
        }
    )
    def get(self, request, *args, **kwargs):
        # Get user and guest_id
        user = request.user if request.user.is_authenticated else None
        guest_id = request.headers.get('Guest-Id')
        
        # Validate guest_id format if provided
        if guest_id and not user:
            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response(
                    {'detail': 'Invalid guest ID format'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get count based on user type
        if user:
            count = Wishlist.objects.filter(user=user).count()
        elif guest_id:
            count = Wishlist.objects.filter(guest_id=guest_id, user__isnull=True).count()
        else:
            count = 0
            
        return Response({'count': count}, status=status.HTTP_200_OK)