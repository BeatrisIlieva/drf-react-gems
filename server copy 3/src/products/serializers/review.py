from cloudinary.utils import cloudinary_url

from rest_framework import serializers

from src.products.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'rating',
            'comment',
            'created_at',
            'content_type',
            'object_id',
            'photo_url',
            'user_full_name'
        ]
        read_only_fields = ['user', 'created_at']

    def get_photo_url(self, obj):
        if obj.user.userphoto.photo:
            return cloudinary_url(obj.user.userphoto.photo.public_id)[0]
        return None

    def get_user_full_name(self, obj):
        if obj.user.userprofile.first_name and obj.user.userprofile.last_name:
            return f'{obj.user.userprofile.first_name} {obj.user.userprofile.last_name}'
        return None
