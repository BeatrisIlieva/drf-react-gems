from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from src.wishlists.models import Wishlist
from src.wishlists.serializers import WishlistSerializer
from src.wishlists.services import WishlistService
from src.wishlists.constants import WishlistErrorMessages


class WishlistViewSet(viewsets.ModelViewSet):
    """
    This ViewSet provides CRUD operations for wishlist items and supports
    both authenticated users and guest users. It includes custom actions
    for removing items and getting wishlist count.

    Key Features:
    - Full CRUD operations for wishlist items
    - Support for both authenticated and guest users
    - Custom actions for item removal and count retrieval
    - Proper error handling and validation
    - User identification through WishlistService
    """

    # Use WishlistSerializer for data serialization
    serializer_class = WishlistSerializer

    # Allow both authenticated and guest users to access wishlist
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        This method filters wishlist items based on whether the request
        is from an authenticated user or guest user. It uses the
        WishlistService to determine user identification and returns
        appropriate filtered queryset.
        """
        try:
            # Get user identification filters (user or guest_id)
            user_filters = WishlistService.get_user_identifier(self.request)

            # Filter wishlist items by user and optimize with select_related
            return Wishlist.objects.filter(**user_filters).select_related(
                'content_type', 'user'
            )
        except ValidationError:
            # Return empty queryset if user identification fails
            return Wishlist.objects.none()

    def create(self, request, *args, **kwargs):
        """
        This method adds a new item to the user's wishlist after validating
        the request data and ensuring the item doesn't already exist.
        """
        try:
            # Get user identification filters
            user_filters = WishlistService.get_user_identifier(request)

            # Validate request data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Extract validated data
            content_type = serializer.validated_data['content_type']
            object_id = serializer.validated_data['object_id']

            # Create wishlist item using service
            wishlist_item = WishlistService.create_wishlist_item(
                user_filters, content_type, object_id
            )

            # Serialize and return response
            response_serializer = self.get_serializer(wishlist_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Return validation error details
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['delete'],
        url_path='remove/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)'
    )
    def remove_item(self, request, content_type_name=None, object_id=None):
        """
        This custom action removes a specific wishlist item based on
        content type name and object ID. It validates the parameters
        and handles various error cases.
        """
        try:
            # Get user identification filters
            user_filters = WishlistService.get_user_identifier(request)

            try:
                # Convert content_type_name to ContentType object
                content_type = ContentType.objects.get(model=content_type_name)

                # Convert object_id string to integer
                object_id_int = int(object_id) if object_id is not None else 0
            except (ContentType.DoesNotExist, ValueError):
                # Handle invalid content type or object ID
                return Response(
                    {'detail': WishlistErrorMessages.ERROR_INVALID_CONTENT_TYPE_OR_ID},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Delete the wishlist item using service
            WishlistService.delete_wishlist_item(
                user_filters, content_type, object_id_int)

            # Return success response with no content
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            # Return validation error details
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='count'
    )
    def get_wishlist_count(self, request):
        """
        This custom action returns the number of items in the user's
        wishlist, useful for displaying wishlist count in the UI.
        """
        try:
            # Get user identification filters
            user_filters = WishlistService.get_user_identifier(request)

            # Count wishlist items for the user
            count = Wishlist.objects.filter(**user_filters).count()

            # Return count in response
            return Response({'count': count}, status=status.HTTP_200_OK)
        except ValidationError as e:
            # Return validation error details
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
