from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from src.common.permissions import IsOrderManager
from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from src.products.serializers.review_management import (
    ReviewManagementSerializer,
)
from src.products.constants import ReviewErrorMessages


class ReviewViewSet(viewsets.ModelViewSet):
    """
    This ViewSet provides CRUD operations for reviews with role-based access control.
    Regular users can only see and manage their own approved reviews, while
    reviewers can see all reviews and manage approval status.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on user permissions.

        This method determines which serializer to use based on the user's
        permissions. Reviewers get the management serializer with approval
        fields, while regular users get the standard serializer.
        """

        # Check if user is a reviewer and this is a reviewer-specific action
        if self.request.user.has_perm(
            'products.approve_review'
        ) and self.action in ['approve', 'unapprove', 'pending']:
            return ReviewManagementSerializer

        return ReviewSerializer

    def get_queryset(self):
        """
        Get filtered queryset based on user permissions.

        This method returns different querysets based on user permissions:
        - Regular users: Only their own reviews
        - Reviewers: All reviews (approved and unapproved)
        """

        # Check if user is a reviewer
        if self.request.user.has_perm('products.approve_review'):
            # Reviewers can see all reviews
            return Review.objects.all().select_related(
                'user',
                'content_type',
                'user__userprofile',
                'user__userphoto',
            )
        else:
            # Regular users can only see their own reviews
            return Review.objects.filter(
                user=self.request.user
            ).select_related(
                'user',
                'content_type',
                'user__userprofile',
                'user__userphoto',
            )

    def create(self, request, *args, **kwargs):
        """
        Create a new review.

        Regular users can create reviews, but they start as unapproved.
        Reviewers can create reviews and set approval status.

        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create the review with user
            review = serializer.save(user=request.user)

            response_serializer = self.get_serializer(review)

            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        """
        Update an existing review.

        Regular users can only update their own reviews.
        Reviewers can update any review and change approval status.
        When a regular user updates a review, it becomes unapproved again.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # If the user is not a reviewer, set approved to False
        if not request.user.has_perm('products.approve_review'):
            serializer.save(approved=False)
        else:
            serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a review.

        Regular users can only delete their own reviews.
        Reviewers can delete any review.
        """
        return super().destroy(request, *args, **kwargs)

    # The @action decorator is used here to add a custom endpoint to the ViewSet.
    # Standard CRUD actions (list, retrieve, create, update, delete) do not cover the use case of fetching
    # the current user's review for a specific product (by content type and object ID).
    # @action allows us to define a flexible, RESTful, and organized custom route for this special workflow.
    # This keeps the API clean and groups related logic together in the ViewSet.
    @action(
        detail=False,
        methods=['get'],
        url_path='user-review/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)',
    )
    def get_user_review(self, request, content_type_name=None, object_id=None):
        """
        Custom action to retrieve the current user's review for a specific product.

        - Exposed as a GET endpoint at /user-review/<content_type_name>/<object_id>/
        - content_type_name: The model name of the product type (e.g., 'earwear', 'neckwear')
        - object_id: The primary key of the product instance

        Workflow:
        1. Validates the content type and object ID from the URL.
        2. Looks up the review for the current user, product type, and product ID.
        3. If found, returns the serialized review data.
        4. If not found, returns a 404 error with a helpful message.
        """
        try:
            # Get the ContentType object for the given model name (e.g., 'earwear')
            content_type = ContentType.objects.get(model=content_type_name)
            object_id_int = int(object_id) if object_id is not None else None
        except (ContentType.DoesNotExist, ValueError):
            # Invalid content type or object ID
            return Response(
                {
                    'error': ReviewErrorMessages.ERROR_INVALID_CONTENT_TYPE_OR_ID
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Look up the review for the current user and product
            review = Review.objects.get(
                user=request.user,
                content_type=content_type,
                object_id=object_id_int,
            )
            serializer = self.get_serializer(review)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except Review.DoesNotExist:
            # No review found for this user and product
            return Response(
                {
                    'error': ReviewErrorMessages.ERROR_REVIEW_NOT_FOUND,
                },
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(detail=True, methods=['post'], permission_classes=[IsOrderManager])
    def approve(self, request, pk=None):
        """
        Approve a review (reviewers only).

        This action allows reviewers to approve reviews, making them
        visible to regular users. Only users with reviewer permissions
        can access this endpoint.

        """
        try:
            review = self.get_object()
            review.approved = True
            review.save()

            return Response(
                {
                    'message': 'Review approved successfully',
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to approve review',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=['post'], permission_classes=[IsOrderManager])
    def unapprove(self, request, pk=None):
        """
        Unapprove a review (reviewers only).

        This action allows reviewers to unapprove reviews, making them
        invisible to regular users. Only users with reviewer permissions
        can access this endpoint.
        """
        try:
            review = self.get_object()
            review.approved = False
            review.save()

            return Response(
                {
                    'message': 'Review unapproved successfully',
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to unapprove review',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=['get'], permission_classes=[IsOrderManager])
    def pending(self, request):
        """
        Get all pending (unapproved) reviews (reviewers only).

        This action returns all reviews that haven't been approved yet.
        Only users with reviewer permissions can access this endpoint.
        """
        pending_reviews = Review.objects.filter(approved=False).select_related(
            'user',
            'content_type',
            'user__userprofile',
            'user__userphoto',
        )

        serializer = ReviewManagementSerializer(pending_reviews, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
