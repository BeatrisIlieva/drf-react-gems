from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from src.wishlists.models import Wishlist
from src.wishlists.serializers import WishlistSerializer
from src.wishlists.services import WishlistService


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        try:
            user_filters = WishlistService.get_user_identifier(self.request)
            return Wishlist.objects.filter(**user_filters).select_related(
                'content_type', 'user'
            ).prefetch_related('product')
        except ValidationError:
            return Wishlist.objects.none()

    def create(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['delete'], url_path='remove/(?P<content_type_name>[^/.]+)/(?P<object_id>[^/.]+)')
    def remove_item(self, request, content_type_name=None, object_id=None):
        try:
            user_filters = WishlistService.get_user_identifier(request)

            try:
                content_type = ContentType.objects.get(model=content_type_name)
                object_id = int(object_id)
            except (ContentType.DoesNotExist, ValueError):
                return Response(
                    {'detail': 'Invalid content type or object ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            WishlistService.delete_wishlist_item(
                user_filters, content_type, object_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='count')
    def get_wishlist_count(self, request):
        try:
            user_filters = WishlistService.get_user_identifier(request)
            count = Wishlist.objects.filter(**user_filters).count()
            return Response({'count': count}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
