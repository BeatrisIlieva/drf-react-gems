from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # For update/delete operations, users can access their own reviews regardless of approval
            if hasattr(self, 'request') and self.request.user.is_authenticated:
                return Review.objects.filter(user=self.request.user).select_related(
                    'user', 'content_type', 'user__userprofile', 'user__userphoto'
                )
        
        # For all other operations (list, retrieve), only show approved reviews
        return Review.objects.filter(approved=True).select_related(
            'user', 'content_type', 'user__userprofile', 'user__userphoto'
        )

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            validated_data = serializer.validated_data
            content_type = validated_data['content_type']
            object_id = validated_data['object_id']
            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=object_id
            ).first()
            
            if existing_review:
                return Response(
                    {'error': 'You have already reviewed this product'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the review
            review = serializer.save(user=request.user)
            response_serializer = self.get_serializer(review)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        instance = self.get_object()
        
        # Check if user owns this review
        if instance.user != request.user:
            return Response(
                {'error': 'You can only update your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        instance = self.get_object()
        
        # Check if user owns this review
        if instance.user != request.user:
            return Response(
                {'error': 'You can only delete your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='user-review/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)')
    def get_user_review(self, request, content_type_name=None, object_id=None):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            content_type = ContentType.objects.get(model=content_type_name)
            object_id = int(object_id)
        except (ContentType.DoesNotExist, ValueError):
            return Response(
                {'error': 'Invalid content type or object ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            review = Review.objects.get(
                user=request.user,
                content_type=content_type,
                object_id=object_id
            )
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(
                {'error': 'Review not found'},
                status=status.HTTP_404_NOT_FOUND
            )
