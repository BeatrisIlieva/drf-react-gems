from typing import Any, Optional
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from src.wishlists.models import Wishlist
from src.wishlists.serializers import WishlistSerializer
from src.wishlists.services import WishlistService
from src.wishlists.constants import WishlistErrorMessages


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]

    def get_queryset(
        self
    ) -> Any:
        try:
            user_filters = WishlistService.get_user_identifier(self.request)
            return Wishlist.objects.filter(**user_filters).select_related(
                'content_type', 'user'
            )
        except ValidationError:
            return Wishlist.objects.none()

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        try:
            user_filters = WishlistService.get_user_identifier(request)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            content_type = serializer.validated_data['content_type']
            object_id = serializer.validated_data['object_id']
            wishlist_item = WishlistService.create_wishlist_item(
                user_filters, content_type, object_id
            )
            response_serializer = self.get_serializer(wishlist_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['delete'],
        url_path='remove/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)'
    )
    def remove_item(
        self,
        request: Request,
        content_type_name: Optional[str] = None,
        object_id: Optional[str] = None
    ) -> Response:
        try:
            user_filters = WishlistService.get_user_identifier(request)
            try:
                content_type = ContentType.objects.get(model=content_type_name)
                object_id_int: int = int(object_id) if object_id is not None else 0
            except (ContentType.DoesNotExist, ValueError):
                return Response(
                    {'detail': WishlistErrorMessages.ERROR_INVALID_CONTENT_TYPE_OR_ID},
                    status=status.HTTP_400_BAD_REQUEST
                )
            WishlistService.delete_wishlist_item(
                user_filters, content_type, object_id_int)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='count'
    )
    def get_wishlist_count(
        self,
        request: Request
    ) -> Response:
        try:
            user_filters = WishlistService.get_user_identifier(request)
            count: int = Wishlist.objects.filter(**user_filters).count()
            return Response({'count': count}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
