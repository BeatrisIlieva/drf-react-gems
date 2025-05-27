from src.products.models.review import Review
from src.products.serializers.review import ReviewSerializer
from rest_framework import permissions
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    # GET /api/reviews/?content_type=7&object_id=123
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        content_type_id = self.request.query_params.get('content_type_id')
        object_id = self.request.query_params.get('object_id')

        if content_type_id and object_id:
            queryset = queryset.filter(
                content_type_id=content_type_id, object_id=object_id)
        return queryset
