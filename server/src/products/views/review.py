from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from typing import Any, Optional

from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from src.products.serializers.review_management import ReviewManagementSerializer
from src.products.constants import ReviewErrorMessages
from src.common.permissions import IsReviewer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product reviews.
    
    This ViewSet provides CRUD operations for reviews with role-based access control.
    Regular users can only see and manage their own approved reviews, while
    reviewers can see all reviews and manage approval status.
    
    Key Features:
    - Role-based review visibility (regular users vs reviewers)
    - Review approval system for content moderation
    - User-specific review management
    - Proper error handling and validation
    """
    
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on user permissions.
        
        This method determines which serializer to use based on the user's
        permissions. Reviewers get the management serializer with approval
        fields, while regular users get the standard serializer.
        
        Returns:
            Serializer class appropriate for the user's permissions
        """
        # Check if user is a reviewer and this is a reviewer-specific action
        if (self.request.user.has_perm('products.approve_review') and 
            self.action in ['approve', 'unapprove', 'pending']):
            return ReviewManagementSerializer
        return ReviewSerializer

    def get_queryset(self) -> Any:
        """
        Get filtered queryset based on user permissions.
        
        This method returns different querysets based on user permissions:
        - Regular users: Only their own reviews
        - Reviewers: All reviews (approved and unapproved)
        
        Returns:
            QuerySet filtered by user permissions
        """
        # Check if user is a reviewer
        if self.request.user.has_perm('products.approve_review'):
            # Reviewers can see all reviews
            return Review.objects.all().select_related(
                'user',
                'content_type',
                'user__userprofile',
                'user__userphoto'
            )
        else:
            # Regular users can only see their own reviews
            return Review.objects.filter(
                user=self.request.user
            ).select_related(
                'user',
                'content_type',
                'user__userprofile',
                'user__userphoto'
            )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new review.
        
        Regular users can create reviews, but they start as unapproved.
        Reviewers can create reviews and set approval status.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            Response with created review data
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create the review with user
            review = serializer.save(user=request.user)
            
            response_serializer = self.get_serializer(review)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update an existing review.
        
        Regular users can only update their own reviews.
        Reviewers can update any review and change approval status.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            Response with updated review data
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Delete a review.
        
        Regular users can only delete their own reviews.
        Reviewers can delete any review.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            Response indicating successful deletion
        """
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get'],
        url_path='user-review/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)'
    )
    def get_user_review(
        self,
        request: Request,
        content_type_name: Optional[str] = None,
        object_id: Optional[str] = None
    ) -> Response:
        try:
            content_type = ContentType.objects.get(model=content_type_name)
            object_id_int = int(object_id) if object_id is not None else None
        except (ContentType.DoesNotExist, ValueError):
            return Response(
                {'error': ReviewErrorMessages.ERROR_INVALID_CONTENT_TYPE_OR_ID},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            review = Review.objects.get(
                user=request.user,
                content_type=content_type,
                object_id=object_id_int
            )
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(
                {'error': ReviewErrorMessages.ERROR_REVIEW_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[IsReviewer])
    def approve(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Approve a review (reviewers only).
        
        This action allows reviewers to approve reviews, making them
        visible to regular users. Only users with reviewer permissions
        can access this endpoint.
        
        Args:
            request: The HTTP request object
            pk: The primary key of the review to approve
            
        Returns:
            Response indicating successful approval
        """
        try:
            review = self.get_object()
            review.approved = True
            review.save()
            
            return Response(
                {'message': 'Review approved successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to approve review'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], permission_classes=[IsReviewer])
    def unapprove(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Unapprove a review (reviewers only).
        
        This action allows reviewers to unapprove reviews, making them
        invisible to regular users. Only users with reviewer permissions
        can access this endpoint.
        
        Args:
            request: The HTTP request object
            pk: The primary key of the review to unapprove
            
        Returns:
            Response indicating successful unapproval
        """
        try:
            review = self.get_object()
            review.approved = False
            review.save()
            
            return Response(
                {'message': 'Review unapproved successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to unapprove review'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], permission_classes=[IsReviewer])
    def pending(self, request: Request) -> Response:
        """
        Get all pending (unapproved) reviews (reviewers only).
        
        This action returns all reviews that haven't been approved yet.
        Only users with reviewer permissions can access this endpoint.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response with list of pending reviews
        """
        pending_reviews = Review.objects.filter(approved=False).select_related(
            'user',
            'content_type',
            'user__userprofile',
            'user__userphoto'
        )
        
        serializer = ReviewManagementSerializer(pending_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
