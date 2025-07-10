from typing import Any, Optional
from rest_framework import serializers

from cloudinary.utils import cloudinary_url

from src.accounts.models.user_photo import UserPhoto


class PhotoSerializer(serializers.ModelSerializer):
    photo_url: serializers.SerializerMethodField = serializers.SerializerMethodField()
    user: serializers.StringRelatedField = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserPhoto
        fields: list[str] = [
            'user',
            'photo',
            'photo_url'
        ]
        read_only_fields: list[str] = [
            'user'
        ]

    def get_photo_url(
        self,
        obj: UserPhoto
    ) -> Optional[str]:
        if obj.photo:
            return cloudinary_url(obj.photo.public_id)[0]
        return None
