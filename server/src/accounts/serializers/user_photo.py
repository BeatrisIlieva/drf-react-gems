from cloudinary.utils import cloudinary_url
from src.accounts.models.user_photo import UserPhoto
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserPhoto
        fields = ['user', 'photo', 'photo_url']
        read_only_fields = ['user']

    def get_photo_url(self, obj):
        if obj.photo:
            return cloudinary_url(obj.photo.public_id)[0]
        return None
