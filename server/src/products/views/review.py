from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from typing import Any, Optional

from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from src.products.constants import ReviewErrorMessages


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self) -> Any:
        return Review.objects.filter(
            user=self.request.user
        ).select_related(
            'user',
            'content_type',
            'user__userprofile',
            'user__userphoto'
        )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            review = serializer.save(user=request.user)
            response_serializer = self.get_serializer(review)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
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
