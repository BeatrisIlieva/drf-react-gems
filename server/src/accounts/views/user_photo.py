from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from src.accounts.models.user_photo import UserPhoto
from src.accounts.serializers.user_photo import PhotoSerializer


class PhotoUploadView(RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        photo, _ = UserPhoto.objects.get_or_create(
            user=self.request.user
        )

        return photo
